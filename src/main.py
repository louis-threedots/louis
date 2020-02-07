
import time
import speech_recognition as sr
from audio import Audio
import os





def main():
    print("Louis has started. Listening for voice commands ...")
    audio = Audio()
    #time.sleep(6)
    audio.speak("Welcome to Louis the brailliant assistant. You can now open any application using voice commands.") 
   
    while (True):
        print("Listening")
        response = audio.recognize_speech()
        if response["transcription"] is not None:
            before_keyword, keyword, app_name = response["transcription"].partition("open")
            if (app_name != ""):
                app_name = app_name.replace(" ","")
                audio.speak("Opening the application"+app_name)


if __name__ == "__main__":
    main()
