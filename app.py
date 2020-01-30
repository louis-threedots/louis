from abc import ABC, abstractmethod
import speech_recognition as sr

# Abstract class that defines the methods amd attributes of Braille Apps. 
class App(ABC):

    def __init__(self, recognizer, microphone):
        self.recognizer = recognizer
        self.microphone = microphone


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


    def recognize_speech():
        """Transcribe speech recorded from `microphone`.

        Returns a dictionary with three keys:
        "success": a boolean indicating whether or not the API request was
                successful
        "error":   `None` if no error occurred, otherwise a string containing
                an error message if the API could not be reached or
                speech was unrecognizable
        "transcription": `None` if speech could not be transcribed,
                otherwise a string containing the transcribed text
        """

        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        with self.microphone as source:
            recognizer.adjust_for_ambient_noise(source) # Already done in main?
            audio = recognizer.listen(source)

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
        #     update the response object accordingly
        try:
            response["transcription"] = recognizer.recognize_google(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # Speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response
