import string
import time
from app import App


class Alphabet(App):

    def on_start(self): 
        # instruction when app started, skip when the user says skip
        #self.app_instruction()

        self.audio.speak("Lets learn the lowercase alphabet first.")
        for c in string.ascii_lowercase:
            self.cells[1].print_character(c)
            self.audio.speak("This is letter " + c)
            time.sleep(5)

        self.audio.speak("Now lets learn punctuation characters.")
        for p in self.punctuation():
            self.cells[1].print_character(c)
            self.audio.speak("This is " + self.punctuation_pronunciation().get(p))
            time.sleep(10)

        self.audio.speak("Now lets learn special charaters.")
        for s in ['CAPITAL', 'LETTER', 'NUMBER', 'ou']:
            self.cells[1].print_character(c)
            self.audio.speak("This represents " + s)
            time.sleep(10)

    def app_instruction(self):
        
        self.audio.speak("Would you like to listen to an instruction for this application?")
        answer = self.audio.recognize_speech()["transcription"]

        # take answer from the user
        if answer == 'yes':
            self.audio.speak("Welcome to Learn. Here you will learn the alphabet.")
        elif answer == 'no':
            self.audio.speak("skipping instruction")
        else:
            self.audio.speak("Wrong answer. Please respond again.")

   
    def on_quit(self):
        print("Quitting")


    def punctuation(self):
        return ['.', ',', ';', ':', '/', '?', '!', '@', '#', '+', '-', '*', '<', '>', '(', ')', ' ']

    def special_characters(self):
        return 

    def punctuation_pronunciation(self):
        return {
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
            ' ': "blank space"
        }
