import string
import time
from app import App
from characters import pronunciation

class Alphabet(App):

    def on_start(self):
        # instruction when app started, skip when the user says skip
        self.app_instruction("Here you will learn the alphabet. You can move on to the next character by saying next.")

        self.audio.speak("Lets learn the lowercase alphabet first.")
        for c in string.ascii_lowercase:
            for cell in reversed(self.cells):
                cell.print_character(c)
            time.sleep(2) # TODO: Arduino needs to send a message to the PC to tell it when a move has completed
            self.audio.speak("This is the letter " + pronunciation[c])
            self.wait_for("next")

        self.audio.speak("Now lets learn punctuation characters.")
        for p in self.punctuation():
            for cell in reversed(self.cells):
                cell.print_character(p)
            time.sleep(2) # TODO: Arduino needs to send a message to the PC to tell it when a move has completed
            self.audio.speak("This is a " + pronunciation[p])
            self.wait_for("next")

        self.audio.speak("Now lets learn special characters.")
        for s in ['CAPITAL', 'LETTER', 'NUMBER']:
            for cell in reversed(self.cells):
                cell.print_character(s)
            time.sleep(2) # TODO: Arduino needs to send a message to the PC to tell it when a move has completed
            self.audio.speak("This announces a " + s)
            self.wait_for("next")

        self.audio.speak("That were all the characters. The app will now close itself.")
        self.on_quit()

    def wait_for(self, word):
        word_pos = -1
        while (word_pos == -1):
            print("Listening ...")
            word_listener = self.audio.recognize_speech()["transcription"]
            word_pos = word_listener.find(word)
            if word_listener.find('quit') != -1 or word_listener.find('exit') != -1:
                self.confirm_quit()

    def punctuation(self):
        return ['.', ',', ';', ':', '/', '?', '!', '@', '#', '+', '-', '*', '<', '>', '(', ')', ' ']

    def special_characters(self):
        return
