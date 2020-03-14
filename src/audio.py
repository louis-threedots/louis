import time
import hashlib
import os
try:
    import speech_recognition as sr
    from gtts import gTTS
    from pygame import mixer
except:
    print('no speech recognition import')

input_speech = False
output_audio = False

class Audio():

    def __init__(self):
        if input_speech:
            self.recognizer =  sr.Recognizer()
            self.microphone = sr.Microphone() # Set appropriate device index, e.g `device_index=3`
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
        # self.recognizer.energy_threshold = 900
        self.cache_dir = "cache"
        if not os.path.exists('src/' + self.cache_dir):
            os.makedirs(self.cache_dir)


    def start_background_listening(self, callback):
        self.stop_listening = self.recognizer.listen_in_background(self.microphone, callback)


    def stop_background_listening(self):
        self.stop_listening

    def speak(self, text):
        if output_audio:
            hash_object = hashlib.md5(text.encode())
            filename = os.path.join(self.cache_dir, hash_object.hexdigest()+".mp3")
            if not(os.path.isfile(filename)):
                print(hash_object.hexdigest())
                open_speech = gTTS(text=text, lang="en", slow=False)
                open_speech.save(filename)
            print("speaking")
            self.playsound(filename)
            print("speaking done")

        print('------ AUDIO OUTPUT ------')
        print(text)
        print('--------------------------')


    def playsound(self, filename):
        mixer.init()
        mixer.music.load(filename)
        mixer.music.play()
        while mixer.music.get_busy() == True:
            continue


    def recognize_speech(self, app = None, keywords = []):
        """Transcribe speech recorded from `microphone`.

        Returns a dictionary with three keys:
        "success": a boolean indicating whether or not the API request was
                successful
        "error":   `None` if no error occurred, otherwise a string containing
                an error message if the API could not be reached or
                speech was unrecognizable
        "transcription": '' if speech could not be transcribed,
                otherwise a string containing the transcribed text
        """

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": "",
        }

        if input_speech:
            # adjust the recognizer sensitivity to ambient noise and record audio
            # from the microphone
            with self.microphone as source:
                speech = self.recognizer.listen(source, phrase_time_limit=4)

            # try recognizing the speech in the recording
            # if a RequestError or UnknownValueError exception is caught,
            #     update the response object accordingly
            try:
                print("Processing speech...")
                response["transcription"] = self.recognizer.recognize_google(speech)
                print("You said: " + response["transcription"])
            except sr.RequestError:
                # API was unreachable or unresponsive
                print("API unavailable")
                response["success"] = False
                response["error"] = "API unavailable"
            except sr.UnknownValueError:
                # Speech was unintelligible
                print("Speech unintelligible")
                response["error"] = "Unable to recognize speech"
        else:
            response["transcription"] = str(input("speech? "))

        # quit / exit command listener
        if app is not None and response["transcription"].find('quit') != -1 or response["transcription"].find('exit') != -1:
            app.confirm_quit()

        return response
