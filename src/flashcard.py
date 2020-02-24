from src.audio import Audio
import random
import time
from src.cell import Cell
from src.apps.learn import Learn

class Flashcard():

    def __init__(self):
        pass

    def play_flashcard(self):
        audio = Audio()
        #cell = Cell()
        learn = Learn()
        audio.start_background_listening('stop')  # todo: test if this works

        # instruction when app started
        # skip when the user says skip
        self.app_instruction()

        # initialise good_pile and bad_pile
        good_pile = []
        bad_pile = []

        print(self.characters_shuffled())
        for c in self.characters_shuffled():
            # initialise variables for each question
            chances = 3
            score = 0
            # display each character
            #cell.rotate(c)
            print("cell displaying letter "+c)
            audio.speak('What letter is this?')
            while chances > 0:
                if chances < 3:
                    audio.speak('Again, what letter is this?')
                if audio.recognize_speech()["transcription"] == c:
                    audio.speak('correct answer! Moving on to the next question.')
                    good_pile.append(c)
                    score += score
                    break
                elif audio.recognize_speech()["transcription"] != c:
                    if chances > 0:
                        chances -= 1
                        if chances == 2:
                            audio.speak("Wrong answer. You have "+str(chances)+" more chances to respond.")
                        elif chances == 1:
                            audio.speak("Wrong answer. You have "+str(chances)+" more chances to respond.")
                        elif chances == 0:
                            if c not in learn.punctuation():
                                audio.speak("You have used all your chances to answer. The correct answer is " + c)
                            else:
                                audio.speak("You have used all your chances to answer. The correct answer is " + learn.punctuation_pronunciation().get(c))
                            audio.speak("I will save this character for later.")
                            bad_pile.append(c)
                            audio.speak("Moving on to the next question.")
                            break
                else:
                    audio.speak("I didn't quite get that. Please respond again.")

        self.test_done_instruction(bad_pile, score)

    def app_instruction(self):
        instruction = "Welcome to the Flashcard App. The purpose of this application is to test how much have you learnt from Learn. Let's start testing. Blah Blah"
        audio = Audio()
        audio.speak("Welcome to the Flashcard app. Would you like to listen to the instruction?")

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

        audio = Audio()
        cell = Cell()
        audio.speak("Testing is done. You got" + round(score * 100 / len(self.characters_shuffled()), 1) + " percent right. Would you like to go through letters you got wrong?")
        if audio.recognize_speech()["transcription"] == "yes":
            audio.speak("Okay, lets go through the characters you answered wrong.")
            while audio.recognize_speech()["transcription"] != "stop application":
                for c in bad_pile:
                    if c not in Learn.punctuation():
                        #cell.rotate(c)
                        print("cell displaying letter " + c)
                        audio.speak("This is " + c)
                        time.sleep(10)
                    else:
                        #cell.rotate(c)
                        print("cell displaying letter " + c)
                        audio.speak("This is "+Learn.punctuation_pronunciation().get(c))
                        time.sleep(10)

        elif audio.recognize_speech()["transcription"] == "no":
            audio.speak("Would you like to exit Flashcard?")
            if audio.recognize_speech()["transcription"] == "yes":
                self.exit_flashcard()
            elif audio.recognize_speech()["transcription"] == "no":
                audio.speak("do you want to take a test again?")
                if audio.recognize_speech()["transcription"] == "yes":
                    self.play_flashcard()
                elif audio.recognize_speech()["transcription"] == "no":
                    self.exit_flashcard()

    def exit_flashcard(self):
        audio = Audio()
        audio.speak("Turning off Flashcard")
        # todo: switch to waiting mode / ready to open other applications

    def characters_shuffled(self):
        learn = Learn()
        chars = learn.alphabet_lowercase() + learn.punctuation() + learn.special_characters()
        chars_shuffled = random.sample(chars, len(chars))
        return chars_shuffled
