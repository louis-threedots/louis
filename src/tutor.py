from audio import Audio
import random
import time
from app import App
from alphabet import Alphabet
import string

class Tutor(App):

    def on_start(self):
        # todo: to be implemented shortly
        #self.audio.start_background_listening('stop')

        # instruction when app started, skip when user says skip
        self.app_instruction()

        # initialise good_pile and bad_pile
        good_pile = []
        bad_pile = []

        print(self.characters_shuffled())
        score = 0
        for c in self.characters_shuffled():
            # initialise variables for each question
            chances = 3
            # display each character
            self.cells[1].print_character(c)
            print("cell displaying letter "+c)
            self.audio.speak('What letter is this?')
            while chances > 0:
                if self.audio.recognize_speech()["transcription"] == c:
                    self.audio.speak('correct answer! Moving on to the next question.')
                    good_pile.append(c)
                    score += 1
                    break
                elif self.audio.recognize_speech()["transcription"] != c:
                    if chances > 0:
                        chances -= 1
                        if chances == 2:
                            self.audio.speak("Wrong answer. You have "+str(chances)+" more chances to respond.")
                        elif chances == 1:
                            self.audio.speak("Wrong answer. You have "+str(chances)+" more chances to respond.")
                        elif chances == 0:
                            if c not in self.punctuation():
                                self.audio.speak("You have used all your chances to answer. The correct answer is " + c)
                            else:
                                self.audio.speak("You have used all your chances to answer. The correct answer is " + learn.punctuation_pronunciation().get(c))
                            self.audio.speak("I will save this character for later.")
                            bad_pile.append(c)
                            self.audio.speak("Moving on to the next question.")
                            break
                else:
                    self.audio.speak("I didn't quite get that. Please respond again.")

        self.test_done_instruction(bad_pile, score)

    def app_instruction(self):
        instruction = "Welcome to the tutor App. The purpose of this application is to test how much have you learnt from Learn. Let's start testing. Blah Blah"
        audio = Audio()
        audio.speak("Welcome to the tutor app. Would you like to listen to the instruction?")

        # take answer from the user
        while True:
            if audio.recognize_speech()["transcription"] == 'yes':
                audio.speak(instruction)
                break
            elif audio.recognize_speech()["transcription"] == 'no':
                audio.speak("skipping instruction")
                break
            elif audio.recognize_speech()["transcription"] != 'yes' and audio.recognize_speech()["transcription"] != 'no':
                audio.speak("Wrong answer. Please respond again.")

    def test_done_instruction(self, bad_pile, score):

        self.audio.speak("Testing is done. You got" + round(score * 100 / len(self.characters_shuffled()), 1) + " percent right. Would you like to go through letters you got wrong?")
        if self.audio.recognize_speech()["transcription"] == "yes":
            self.audio.speak("Okay, lets go through the characters you answered wrong.")
            while self.audio.recognize_speech()["transcription"] != "stop application":
                for c in bad_pile:
                    if c not in self.punctuation():
                        self.cells[1].print_character(c)
                        print("cell displaying letter " + c)
                        self.audio.speak("This is " + c)
                        time.sleep(10)
                    else:
                        self.cells[1].print_character(c)
                        print("cell displaying letter " + c)
                        self.audio.speak("This is "+self.punctuation_pronunciation().get(c))
                        time.sleep(10)

        elif self.audio.recognize_speech()["transcription"] == "no":
            self.audio.speak("Would you like to exit tutor?")
            if self.audio.recognize_speech()["transcription"] == "yes":
                self.on_quit()
            elif self.audio.recognize_speech()["transcription"] == "no":
                self.audio.speak("do you want to take a test again?")
                if self.audio.recognize_speech()["transcription"] == "yes":
                    self.on_quit()
                elif self.audio.recognize_speech()["transcription"] == "no":
                    self.on_quit()

    def on_quit(self):
        self.audio.speak("Turning off tutor")

    def characters_shuffled(self):
        chars = string.ascii_lowercase + self.punctuation() + ['CAPITAL', 'LETTER', 'NUMBER', 'ou']
        chars_shuffled = random.sample(chars, len(chars))
        return chars_shuffled

    def punctuation(self):
        return ['.', ',', ';', ':', '/', '?', '!', '@', '#', '+', '-', '*', '<', '>', '(', ')', ' ']

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
