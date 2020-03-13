#! /usr/bin/python3
import time
from arduino import Arduino
from cell import Cell

# apps:
from learn import Learn
from tutor import Tutor

def discover():
    print("Louis has started. Running cell discovery ...")
    arduino = Arduino()
    time.sleep(2)
    num_cells = arduino.discover()
    print(num_cells)
    cells = [Cell(i, arduino) for i in range(1,num_cells+1)]
    print("Cell discovery completed. "+str(num_cells)+" cells found.")
    return arduino, cells

def main_menu(arduino, cells, audio):
    audio.speak("You can now open any application using voice commands.")
    while (True):
        print("Listening ...")
        response = audio.recognize_speech()
        if response["transcription"] != "":
            before_keyword, keyword, app_name = response["transcription"].partition("open")
            if app_name != '': # found command 'open'
                open_app(app_name, cells, audio, arduino)

def open_app(app_name, cells, audio, arduino):
    current_app = None

    app_name = app_name.replace(" ", "")
    if app_name == 'learn':
        current_app = Learn("Learn",cells,audio,arduino)
    elif app_name == 'tutor':
        current_app = Tutor("Tutor",cells,audio,arduino)

    if current_app is not None:
        audio.speak("Opening the application " + app_name)
        current_app.on_start()
    else:
        audio.speak("I did not recognize the app. Could you try to open the app again?")
