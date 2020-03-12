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
            self.wait_for_all_cells_finished()
            self.audio.speak("This is the letter " + pronunciation[c])
            self.wait_for_audio("next")

        self.audio.speak("Now lets learn punctuation characters.")
        for p in self.punctuation():
            for cell in reversed(self.cells):
                cell.print_character(p)
            self.wait_for_all_cells_finished()
            self.audio.speak("This is a " + pronunciation[p])
            self.wait_for_audio("next")

        self.audio.speak("Now lets learn special characters.")
        for s in ['CAPITAL', 'LETTER', 'NUMBER']:
            for cell in reversed(self.cells):
                cell.print_character(s)
            self.wait_for_all_cells_finished()
            self.audio.speak("This announces a " + s)
            self.wait_for_audio("next")

        self.audio.speak("That were all the characters. The app will now close itself.")
        self.on_quit()

    def punctuation(self):
        return ['.', ',', ';', ':', '/', '?', '!', '@', '#', '+', '-', '*', '<', '>', '(', ')', ' ']

    def special_characters(self):
        return
