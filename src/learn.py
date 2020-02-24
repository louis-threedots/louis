from src.audio import Audio
import string
import time
from src.cell import Cell

class Learn():

    def __init__(self):
        pass

    def play_learn(self):
        audio = Audio()
        cell = Cell()
        # todo: app should stop whenever the user says "stop application"
        audio.start_background_listening('stop')  # todo: test if this works

        # instruction when app started, skip when the user says skip
        self.app_instruction()

        audio.speak("Lets learn lowercase alphabet first.")
        for c in self.alphabet_lowercase():
            cell.rotate(c)
            audio.speak("This is " + c)
            time.sleep(10)

        audio.speak("Now lets learn punctuation characters.")
        for p in self.punctuation():
            cell.rotate(p)
            audio.speak("This is " + self.punctuation_pronunciation().get(p))
            time.sleep(10)

        audio.speak("Now lets learn special charaters.")
        for s in self.special_characters():
            cell.rotate(s)
            audio.speak("This represents " + s)
            time.sleep(10)

    def app_instruction(self):
        audio = Audio()
        audio.speak("Would you like to listen to the instruction for this application?")

        # take answer from the user
        if audio.recognize_speech()["transcription"] == 'yes':
            audio.speak("Welcome to Learn. Here you will learn alphabet in Braille.")
        elif audio.recognize_speech()["transcription"] == 'no':
            audio.speak("skipping instruction")
        elif audio.recognize_speech()["transcription"] != 'yes' and audio.recognize_speech()["transcription"] != 'no':
            audio.speak("Wrong answer. Please respond again.")

    def learn_done_instruction():
        audio = Audio()
        audio.speak("")

    def alphabet_lowercase(self):
        return list(string.ascii_lowercase)

    def punctuation(self):
        return ['.', ',', ';', ':', '/', '?', '!', '@', '#', '+', '-', '*', '<', '>', '(', ')', ' ']

    def special_characters(self):
        return ['capital', 'letter', 'number', 'ou']

    def punctuation_pronunciation(self):
        punctuation_pronunciation = {
            '.': "dot",
            ',': "comma",
            ';': "semi colon",
            ':': "colon",
            '/': "slash",
            '?': "question mark",
            '!': "exclamation mark",
            '@': "at symbol",
            '#': "hash",
            '+': "plus symbol",
            '-': "minus symbol",
            '*': "asterisk",
            '<': "less than",
            '>': "greater than",
            '(': "left parentheses",
            ')': "right parentheses",
            ' ': "blank"
        }
        return punctuation_pronunciation
