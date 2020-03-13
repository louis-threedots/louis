#! /usr/bin/python3
from audio import Audio
from main_functions import *

def main():
    arduino, cells = discover()
    audio = Audio()
    audio.speak("Welcome to Louis the brailliant assistant.")
    main_menu(arduino, cells, audio)

main()
