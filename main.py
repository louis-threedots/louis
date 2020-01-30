
import time
import speech_recognition as sr
from audio import Audio

# this is called from the background thread
def callback(recognizer, audio):
    print("Processing audio input ...")
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        speech = recognizer.recognize_google(audio)
        print("You said " + speech )
        before_keyword, keyword, app_name = speech.partition("open")
        if (app_name != ""):
            print("Opening the app"+app_name)
        

    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    #TODO: Listen for `open` and `close` to open appropriate apps.




def main():
    print("Louis has started. Listening for voice commands ...")
    audio = Audio()
    audio.start_background_listening(callback)
    while (True): time.sleep(1)

if __name__ == "__main__":
    main()
