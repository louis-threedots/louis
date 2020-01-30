from abc import ABC, abstractmethod
import speech_recognition as sr

# Abstract class that defines the methods amd attributes of Braille Apps. 
class App(ABC):

    def __init__(self, cells, audio):
        self.cells = cells
        self.audio = self.audio


    @abstractmethod
    def on_start(self):
        # Actions that an app wants to perform on app start
        pass

    @abstractmethod
    def on_quit(self):
        # Actions that an app wants to perform when quitting the app
        pass



    def load_state(self, state):
        #TODO: Rehydrate app state from local file system
        pass

    
    def save_state(self, state):
        #TODO: Save app state to local file system
        pass
