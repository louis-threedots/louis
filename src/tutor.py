from src.audio import Audio
from src.characters import pronunciation
from src.characters import pronunciation_to_character
import random
import time
from src.app import App
import string

class Tutor(App):

    def on_start(self):
        # todo: to be implemented shortly
        #self.audio.start_background_listening('stop')

        # instruction when app started, skip when user says skip
        self.app_instruction("The purpose of this application is to test how much you have learnt from Learn. Let's start testing."
                             "You can answer the question with any word of your choice that starts with a letter you believe to be the correct answer,"
                             "but avoid using quit or exit unless you want to quit the application.")

        # initialise good_pile and bad_pile
        good_pile = []
        bad_pile = []

        score = 0
        for c in self.characters_shuffled():
            # initialise variables for each question
            chances = 3
            # display each character
            self.cells[1].print_character(c)
            print("cell displaying letter "+c)

            #give instruction: digit/punctuation/special indicator/alphabet
            if c in self.digit():
                self.audio.speak('What letter is this? This is a digit.')
            elif c in self.punctuation():
                self.audio.speak("What letter is this? This is a punctuation character.")
            elif c in self.special_indicators():
                self.audio.speak("What letter is this? This is a special indicator.")
            else:
                self.audio.speak("What letter is this? This is an alphabet character.")

            while chances > 0:
                answer = self.audio.recognize_speech()["transcription"]
                if answer == '': # speech recognizer returned error
                    self.audio.speak("I didn't quite get that. Please respond again.")
                    continue

                answer = answer.lower()

                #go back to main app when heard quit/exit
                if answer == 'quit' or answer == 'exit':
                    self.audio.speak("Would you like to quit tutor app?")
                    answer_2 = self.audio.recognize_speech()['transcription'].lower()
                    if answer_2 == 'yes':
                        break
                    elif answer_2 == 'no':
                        continue

                if  len(c) == 1: #if the given character is an alphabetical letter
                    # cut down length of input word to one character
                    # to allow 'Apple' for 'A' etc.
                    if c not in self.special_indicators and answer not in self.special_indicators:
                        answer = answer[0]
                    if answer == c:
                        self.audio.speak('You correctly answered ' + pronunciation[c] + '! Moving on to the next question.')
                        good_pile.append(c)
                        score += 1
                        break
                    else:
                        chances -= 1
                        if chances > 0:
                            self.audio.speak("You incorrectly answered " + answer + ". You have " + str(chances) + " more chances to respond.")
                        elif chances == 0:
                            self.audio.speak("You have used all your chances to answer. The correct answer is " + pronunciation[c])
                            self.audio.speak("I will save this character for later.")
                            bad_pile.append(c)
                            self.audio.speak("Moving on to the next question.")

                else:   #if the given character is a digit/punctuation/indicator

                    if pronunciation_to_character.get(answer) == c:
                        self.audio.speak('You correctly answered ' + pronunciation[c] + '! Moving on to the next question.')
                        good_pile.append(c)
                        score += 1
                        break
                    else:
                        chances -= 1
                        if chances > 0:
                            self.audio.speak("You incorrectly answered " + answer + ". You have " + str(chances) + " more chances to respond.")
                        elif chances == 0:
                            self.audio.speak("You have used all your chances to answer. The correct answer is " + pronunciation[c])
                            self.audio.speak("I will save this character for later.")
                            bad_pile.append(c)
                            self.audio.speak("Moving on to the next question.")

        self.test_done_instruction(bad_pile, score)


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
                        self.audio.speak("This is " + pronunciation[c])
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

    def characters_shuffled(self):
        chars = list(string.ascii_lowercase) + self.punctuation() + ['CAPITAL', 'LETTER', 'NUMBER'] + self.digit()
        chars_shuffled = random.sample(chars, len(chars))
        return chars_shuffled

    def punctuation(self):
        return ['.', ',', ';', ':', '/', '?', '!', '@', '#', '+', '-', '*', '<', '>', '(', ')', ' ']

    def digit(self):
        return ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def special_indicators(self):
        return ["capital", "letter", "number"]