
import time
import speech_recognition as sr

r = sr.Recognizer()
m = sr.Microphone() # Set appropriate device index, e.g `device_index=3`.

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
    
    with m as source:
        r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening


# start listening in the background (note that we don't have to do this inside a `with` statement)
    stop_listening = r.listen_in_background(m, callback)
    while (True): time.sleep(1)

if __name__ == "__main__":
    main()
