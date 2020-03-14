from abc import ABC, abstractmethod
from characters import indicator_dict

# Abstract class that defines the methods amd attributes of Braille Apps.
class App(ABC):

    def __init__(self, name, cells, audio, arduino):
        self.cells = cells
        self.audio = audio
        self.arduino = arduino
        self.name = name

    @abstractmethod
    def on_start(self):
        # Actions that an app wants to perform on app start
        pass

    def on_quit(self):
        # Actions that an app wants to perform when quitting the app
        self.audio.speak("The app will now close itself. Goodbye.")
        for cell in reversed(self.cells):
            cell.rotate_to_rel_angle(720 - cell.motor_position)
            cell.set_to_default()
        # return to main thread
        from main_functions import main_menu
        main_menu(self.arduino, self.cells, self.audio)

    def confirm_quit(self):
        self.audio.speak("Would you like to quit this application?")
        #answer = self.audio.recognize_speech()["transcription"]
        response = self.audio.await_response(["yes","no"])
        # take answer from the user
        if response == "yes":
            self.on_quit()
        elif response == "no":
            self.audio.speak("You're returning to the app.")

    def load_state(self, state):
        #TODO: Rehydrate app state from local file system
        pass

    def save_state(self, state):
        #TODO: Save app state to local file system
        pass

    def app_instruction(self, instruction):
        self.audio.speak("Would you like to listen to an instruction for this application?")
        response = self.audio.await_response(['yes','no'])
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

            if len(to_print) == len(self.cells) or i == len(prepared_text)-1 :
                # Letters need to be passed in reverse in order to be processed in parallel
                for j in range(len(to_print)-1,-1,-1):
                    self.cells[j].print_character(to_print[j])
                # Wait for pagination. Exiting turns out to be more difficult since wait_for_button_press blocks the execution.
                self.cells[-1].wait_for_button_press()
                to_print = []
