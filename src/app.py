from abc import ABC, abstractmethod
import os
import json
from characters import indicator_dict, character_dict

# Abstract class that defines the methods amd attributes of Braille Apps.
class App(ABC):

    def __init__(self, name, cells, audio, arduino):
        self.cells = cells
        self.audio = audio
        self.arduino = arduino
        self.name = name
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
        from main_functions import main_menu
        main_menu(self.arduino, self.cells, self.audio)

    def confirm_quit(self):
        self.audio.speak("Would you like to quit this application?")
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
        filename = self.name.lower() + '_state'
        filepath = 'src/app_states/' + filename + '.py'
        if not(os.path.exists(filepath)):
            with open(filepath, 'w') as f:
                settings = {}
                f.write(json.dumps(settings, indent=4, sort_keys=True))
        with open(filepath, 'r') as f:
            return json.loads(f.read())
        # module = getattr(__import__('app_states', fromlist=[filename]), filename)
        # return module.settings

    def save_settings(self):
        # Save app settings to local file system
        filename = self.name.lower() + '_state'
        filepath = 'src/app_states/' + filename + '.py'
        with open(filepath, 'w') as f:
            f.write(json.dumps(self.settings, indent=4, sort_keys=True))

    def app_instruction(self, instruction):
        self.audio.speak("Would you like to listen to an instruction for this application?")
        response = self.await_response(['yes','no'])
        if response == "yes":
            self.audio.speak("Welcome to " + self.name + ". " + instruction)
        elif response == "no":
            self.audio.speak("skipping instruction")

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

    def print_text(self, text):
        prepared_text = []
        for letter in text:
            if letter not in indicator_dict:
                if letter.isupper():
                    prepared_text.append('CAPITAL')
                    letter = letter.lower()
                elif letter.isdigit():
                    prepared_text.append('NUMBER')
            prepared_text.append(letter)

        to_print = []
        for i in range(0,len(prepared_text)):
            to_print.append(prepared_text[i])

            # TODO fix bug where the last characters stay the same as previous pagination when at end of sentence (doesn't go to zero)
            if len(to_print) == len(self.cells) or i == len(prepared_text)-1 :
                # Letters need to be passed in reverse in order to be processed in parallel
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
        invalid = True

        if answer.find("options") != -1:
            desired_response_string = str(desired_responses).strip('[]')
            self.audio.speak("Your options are: " + desired_response_string + '.')
            invalid = False
        # quit / exit command listener
        elif answer.find('quit') != -1 or answer.find('exit') != -1:
            self.confirm_quit()
            invalid = False

        if len(desired_responses) == 0:
            return answer
        else:
            for d_r in desired_responses:
                if answer.find(d_r) != -1:
                    response = d_r
                    print("You said: " + response)
                    return response

        if invalid:
            self.audio.speak("Invalid option, please try again.")

        response = self.await_response(desired_responses)
        return response
