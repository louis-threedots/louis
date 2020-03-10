#! /usr/bin/python3
import time
try:
    import speech_recognition as sr
except:
    print('no speech recognition import')
from audio import Audio
from arduino import Arduino
import os
import asyncio
from cell import Cell

# apps:
from alphabet import Alphabet
from tutor import Tutor

def main():
    print("Louis has started. Running cell discovery ...")
    arduino = Arduino()
    time.sleep(2)
    num_cells = arduino.discover()
    print(num_cells)
    cells = [Cell(i, arduino) for i in range(1,num_cells+1)]
    print("Cell discovery completed. "+str(num_cells)+" cells found.")
    audio = Audio()
    audio.speak("Welcome to Louis the brailliant assistant. You can now open any application using voice commands.")

    while (True):
        print("Listening ...")
        response = audio.recognize_speech()
        if response["transcription"] != "":
            before_keyword, keyword, app_name = response["transcription"].partition("open")
            open_app(app_name, cells, audio, arduino)

def open_app(app_name, cells, audio, arduino):
    current_app = None

    app_name = app_name.replace(" ","")
    if app_name.endswith("app"):
        app_name = app_name[:-3]

    print(app_name)
    if app_name == 'learn':
        current_app = Alphabet("Learn",cells,audio,arduino)
    elif app_name == 'tutor':
        current_app = Tutor("Tutor",cells,audio,arduino)

    if current_app is not None:
        audio.speak("Opening the application " + app_name)
        current_app.on_start()
    else:
        audio.speak("I did not recognize the app. Could you try to open the app again?")

main()
