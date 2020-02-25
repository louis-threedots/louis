
import time
import speech_recognition as sr
from louis.src.audio import Audio
from louis.src.arduino import Arduino
import os
from louis.src.alphabet import Alphabet
import asyncio
from louis.src.cell import Cell


def main():
    print("Louis has started. Running cell discovery ...")
    # audio = Audio()
    arduino = Arduino()
    num_cells = 2 
    #arduino.discover()
    print(num_cells)
    cells = [Cell(i, arduino) for i in range(1,num_cells+1)]
    print("Cell discovery completed."+str(num_cells)+" cells found.")
    audio = Audio()
    audio.speak("Welcome to Louis the brailliant assistant. You can now open any application using voice commands.")
    current_app = Alphabet("Alphabet",cells,audio)
    current_app.on_start()

    while (True):
        print("Listening ...")
        response = audio.recognize_speech()
        if response["transcription"] is not None:
            before_keyword, keyword, app_name = response["transcription"].partition("open")
            if (app_name != ""):
                app_name = app_name.replace(" ","")
                audio.speak("Opening the application"+app_name)


if __name__ == "__main__":
    main()
