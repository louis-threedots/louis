from src.audio import Audio
import string
import random
import time
from src.cell import Cell
from src.learn import Learn
class Flashcard():

    def __init__(self):
        pass

    def play_flashcard(self):
        audio = Audio()
        cell = Cell()
        # todo: app should stop whenever the user says "stop application"
        audio.start_background_listening('stop')  # todo: test if this works

        # instruction when app started
        # skip when the user says skip
        self.app_instruction()

        # initialise good_pile and bad_pile
        good_pile = []
        bad_pile = []
        audio.start_background_listening()

        for c in self.characters_shuffled():
            # initialise variables for each question
            chances = 3
            correct = False
            score = 0
            # display each character
            cell.rotate(c)
            audio.speak('What letter is this?')
            while correct is False or chances > 0:
                if self.take_answer() == c:
                    audio.speak('correct answer! Move on to the next question.')
                    good_pile.append(c)
                    score += score
                    correct = True
                elif self.take_answer() != c:
                    chances -= chances
                    if chances == 0:
                        audio.speak("You have used all your chances to answer. The correct answer is " + c)
                        audio.speak("I will save this character for later.")
                        bad_pile.append(c)
                        audio.speak("Moving on to the next question.")
                        break
                    if chances > 0:
                        audio.speak('Incorrect! you have ' + chances + " more chances to respond")

        self.test_done_instruction(bad_pile, score)

    def app_instruction(self):
        instruction = "Welcome to the Flashcard App. The purpose of this application is to test how much have you learnt from Learn. Let's start testing."
        audio = Audio()
        audio.speak("Would you like to listen to an instruction for this application?")

        # take answer from the user
        if self.take_answer() == 'yes':
            audio.speak(instruction)
        elif self.take_answer() == 'no':
            audio.speak("skipping instruction")
        elif self.take_answer() != 'yes' or self.take_answer() != 'no':
            audio.speak("Wrong answer. Please respond again.")

    def test_done_instruction(self, bad_pile, score):

        audio = Audio()
        cell = Cell()
        audio.speak("Testing is done. You got" + round(score * 100 / len(self.characters_shuffled()), 1) + " percent right. Would you like to go through letters you got wrong?")
        if self.take_answer() == "yes":
            audio.speak("Okay, lets go through the characters you answered wrong.")
            while self.take_answer() != "stop application":
                for c in bad_pile:
                    if c not in Learn.punctuation():
                        cell.rotate(c)
                        audio.speak("This is " + c)
                        time.sleep(10)
                    else:
                        cell.rotate(c)
                        audio.speak("This is "+Learn.punctuation_pronunciation().get(c))
                        time.sleep(10)

        elif self.take_answer() == "no":
            audio.speak("Would you like to exit Flashcard?")
            if self.take_answer() == "yes":
                self.exit_flashcard()
            elif self.take_answer() == "no":
                audio.speak("do you want to take a test again?")
                if self.take_answer() == "yes":
                    self.play_flashcard()
                elif self.take_answer() == "no":
                    self.exit_flashcard()

    def take_answer(self):
        audio = Audio()
        while audio.recognize_speech()["transcription"] is not None:
            answer = audio.recognize_speech()["transcription"]
            break
        return answer

    def exit_flashcard(self):
        audio = Audio()
        audio.speak("Turning off Flashcard")
        audio.start_background_listening()
        # todo: switch to waiting mode / ready to open other applications

    def characters_shuffled(self):
        chars = Learn.alphabet_lowercase() + Learn.punctuation() + Learn.special_characters()
        return random.shuffle(chars, random)
