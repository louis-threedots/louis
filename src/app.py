from abc import ABC, abstractmethod
import os
import json
from characters import indicator_dict, character_dict

# Abstract class that defines the methods amd attributes of Braille Apps.
class App(ABC):

    def __init__(self, name, cells, audio, arduino, mainApp):
        self.cells = cells
        self.audio = audio
        self.arduino = arduino
        self.mainApp = mainApp
        self.name = name
        self.instruction = "Welcome to " + self.name + ". This application does not have instructions yet."
        # settings
        filename = self.name.lower() + '_state'
        self.filepath = os.path.join(os.path.dirname(__file__), 'app_states/' + filename + '.txt')
        self.settings = self.load_settings()

    @abstractmethod
    def on_start(self):
        # Actions that an app wants to perform on app start
        pass

    def on_quit(self):
        # Actions that an app wants to perform when quitting the app
        self.audio.speak("The app will now close itself. Goodbye.")
        self.save_settings()
        self.reset_cells()
        # return to main thread
        self.mainApp.main_menu()

    def confirm_quit(self):
        text = "Would you like to quit this application?"
        if self.name == 'main':
            text = "Would you like to quit louis?"
        self.audio.speak(text)
        response = self.await_response(["yes","no"])
        # take answer from the user
        if response == "yes":
            self.on_quit()
        elif response == "no":
            self.audio.speak("You're returning to the app.")

    def reset_cells(self, to='zero'):
        for cell in reversed(self.cells):
            cell.reset(to=to)

    def load_settings(self):
        # Rehydrate app settings from local file system
        if not(os.path.exists(self.filepath)):
            with open(self.filepath, 'w') as f:
                settings = {}
                f.write(json.dumps(settings, indent=4))
        with open(self.filepath, 'r') as f:
            return json.loads(f.read())

    def save_settings(self):
        # Save app settings to local file system
        with open(self.filepath, 'w') as f:
            f.write(json.dumps(self.settings, indent=4))

    def app_instruction(self):
        self.audio.speak(self.instruction)

    def get_pressed_button(self):
        # Returns the index of the pressed cell button
        return self.arduino.get_pressed_button()

    def wait_for_all_cells_finished(self):
        # Returns true if all the cells have finished rendering
        cells_finished_rotating = [False] * len(self.cells)
        while False in cells_finished_rotating:
            for cell in self.cells:
                cells_finished_rotating[cell.index - 1] = cell.has_finished_rotating()

    def print_character_all_cells(self, c):
        for cell in reversed(self.cells):
            cell.print_character(c)
        self.wait_for_all_cells_finished()
        self.print_cells_to_terminal()

    def print_text(self, text):
        prepared_text = []
        for i,letter in enumerate(text):
            if letter not in indicator_dict:
                if i>=1 and letter.isalpha() and text[i-1].isdigit():
                    prepared_text.append('LETTER')
                
                if letter.isupper():
                    prepared_text.append('CAPITAL')
                    letter = letter.lower()
                elif letter.isdigit():
                    insert_letter_ind = True
                    # indicator not necessary when previous char is digit
                    if i>=1 and text[i-1].isdigit():
                        insert_letter_ind = False
                    # indicator not necessary when part of number (e.g. 1,496.2)
                    if i>=2 and text[i-2].isdigit() and (text[i-1] == '.' or text[i-1] == ','):
                        insert_letter_ind = False
                    if insert_letter_ind:
                        prepared_text.append('NUMBER')
            
            prepared_text.append(letter)

        to_print = []
        for i in range(0,len(prepared_text)):
            to_print.append(prepared_text[i])

            if len(to_print) == len(self.cells) or i == len(prepared_text)-1 :
                # Letters need to be passed in reverse in order to be processed in parallel
                padding = len(self.cells) - len(to_print) 
                to_print = to_print + list(" " * padding)
                for j in range(len(to_print)-1,-1,-1):
                    self.cells[j].print_character(to_print[j])

                self.print_cells_to_terminal()
                # Wait for pagination. Exiting turns out to be more difficult since wait_for_button_press blocks the execution.
                self.cells[-1].wait_for_button_press()
                to_print = []

    def print_cells_to_terminal(self):
        dots_print = ['.', 'o']
        top_row, middle_row, bottom_row, character_row = '', '', '', ''

        for cell in self.cells:
            extra_padding = len(cell.character) - 1
            dots = character_dict[cell.character]['dots']
            character_row = character_row + '  ' + str(cell.character) + '  '

            top_row = top_row + '|' + dots_print[dots[0]] + ' ' + dots_print[dots[3]] + '|' + (' ' * extra_padding)
            middle_row = middle_row + '|' + dots_print[dots[1]] + ' ' + dots_print[dots[4]] + '|' + (' ' * extra_padding)
            bottom_row = bottom_row + '|' + dots_print[dots[2]] + ' ' + dots_print[dots[5]] + '|' + (' ' * extra_padding)

        print(top_row)
        print(middle_row)
        print(bottom_row)
        print(character_row)

    def await_response(self, desired_responses = []):
        answer = self.audio.recognize_speech()["transcription"]
        answer = answer.lower()
        invalid = True

        if answer.find("options") != -1:
            self.audio.speak("Your options are:")
            for option in desired_responses:
                self.audio.speak("- "+option)
            invalid = False
        # quit / exit command listener
        elif answer.find('quit') != -1 or answer.find('exit') != -1:
            self.confirm_quit()
            invalid = False
        # help listener
        elif answer.find('help') != -1:
            self.app_instruction()
            invalid = False

        if len(desired_responses) == 0:
            return answer
        else:
            for d_r in desired_responses:
                if answer.find(d_r) != -1:
                    response = d_r
                    return response

        if answer != "" and invalid:
            self.audio.speak("Invalid option, please try again.")

        response = self.await_response(desired_responses)
        return response
