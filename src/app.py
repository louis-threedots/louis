from abc import ABC, abstractmethod
import speech_recognition as sr

# Abstract class that defines the methods amd attributes of Braille Apps.
class App(ABC):

    def __init__(self, name, cells, audio):
        self.cells = cells
        self.audio = audio
        self.name = name
        self.is_open = True


    @abstractmethod
    def on_start(self):
        # Actions that an app wants to perform on app start
        pass

    def on_quit(self):
        # Actions that an app wants to perform when quitting the app
        self.audio.speak("Goodbye.")
        for cell in self.cells:
            cell.rotate_to_rel_angle(360 - cell.motor_position)
        print("Quitting")

    def confirm_quit(self):

        self.audio.speak("Would you like to quit this application?")
        answer = self.audio.recognize_speech()["transcription"]

        # take answer from the user
        if answer.find('yes') != -1:
            self.on_quit()
        elif answer.find('no') != -1:
            self.audio.speak("You're returning to the app.")
        else:
            self.audio.speak("I did not understand.")
            self.confirm_quit() # ask the question again

    def close():
        self.is_open = false

    def load_state(self, state):
        #TODO: Rehydrate app state from local file system
        pass

    def save_state(self, state):
        #TODO: Save app state to local file system
        pass

    def app_instruction(self, instruction):

        self.audio.speak("Would you like to listen to an instruction for this application?")
        answer = self.audio.recognize_speech()["transcription"]

        # take answer from the user
        if answer.find('yes') != -1:
            self.audio.speak("Welcome to " + self.name + ". " + instruction)
        elif answer.find('no') != -1:
            self.audio.speak("skipping instruction")
        else:
            self.audio.speak("I did not understand.")
            self.app_instruction(instruction) # ask the question again
