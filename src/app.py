from abc import ABC, abstractmethod
import speech_recognition as sr

# Abstract class that defines the methods amd attributes of Braille Apps. 
class App(ABC):

    def __init__(self, name, cells, audio):
        self.cells = cells
        self.audio = self.audio
        self.name = name
        self.is_open = True


    @abstractmethod
    def on_start(self):
        # Actions that an app wants to perform on app start
        pass

    @abstractmethod
    def on_quit(self):
        # Actions that an app wants to perform when quitting the app
        pass

    def close():
        self.is_open = false

    def load_state(self, state):
        #TODO: Rehydrate app state from local file system
        pass

    
    def save_state(self, state):
        #TODO: Save app state to local file system
        pass
