from audio import Audio
from characters import *
import random
import time
from app import App
import string

class Tutor(App):

    def on_start(self):
        # todo: to be implemented shortly
        #self.audio.start_background_listening('stop')

        # instruction when app started, skip when user says skip
        self.app_instruction("""
            The purpose of this application is to test how much you have learnt from Learn. Let's start testing.
            You can answer the question with any word of your choice that starts with the letter you believe to be the correct answer,
            but avoid using quit or exit unless you want to quit the application.
        """)
        self.run_test()

    def run_test(self):
        # initialise good_pile and bad_pile
        good_pile = []
        bad_pile = []

        self.audio.speak("How would you like the length of the test to be? Please choose one of the following: short, medium or full.")
        test_length_reply = self.audio.recognize_speech(app=self)["transcription"]

        if "short" in test_length_reply:
            test_length = "short"
        elif "medium" in test_length_reply:
            test_length = "medium"
        elif "full" in test_length_reply:
            test_length = "full"
        else:
            test_length = "short"

        for (c, chartype) in self.characters_shuffled(test_length=test_length):
            # initialise variables for each question
            chances = 3
            # display the character
            self.print_character_all_cells(c)

            #give instruction: digit/punctuation/special indicator/alphabet
            chartypes_output = {
                'alphabet': 'an alphabet character',
                'punctuation': 'a punctuation character',
                'indicator': 'a special indicator',
                'digit': 'a digit'
            }
            self.audio.speak('What letter is this? This is ' + chartypes_output[chartype] + '.')

            while chances > 0:
                answer = self.audio.recognize_speech(app=self)["transcription"]
                if answer == '': # speech recognizer returned error
                    self.audio.speak("I didn't quite get that. Please respond again.")
                    continue

                answer = answer.lower().strip()

                if chartype == 'alphabet':
                    correct_answer = c
                    # cut down length of input word to one character
                    # to allow 'Apple' for 'A' etc.
                    answer = answer[0]
                elif chartype == 'indicator':
                    correct_answer = c.lower()
                else: # digit or punctuation
                    correct_answer = character_dict[c]['pronunciation']

                if answer == correct_answer:
                    self.audio.speak('You correctly answered ' + character_dict[c]['pronunciation'] + '! Moving on to the next question.')
                    good_pile.append(c)
                    break
                else:
                    answer_output = answer
                    if answer in character_dict: # mainly for 'a' => 'ay'
                        answer_output = character_dict[answer]['pronunciation']

                    chances -= 1
                    if chances > 0:
                        self.audio.speak("You incorrectly answered " + answer_output + ". You have " + str(chances) + " more chances to respond.")
                    else:
                        self.audio.speak("You incorrectly answered " + answer_output + ". You have used all your chances to answer. The correct answer is " + character_dict[c]['pronunciation'])
                        self.audio.speak("I will save this character for later.")
                        bad_pile.append(c)
                        self.audio.speak("Moving on to the next question.")

        self.test_done_instruction(bad_pile, good_pile)

    def test_done_instruction(self, bad_pile, good_pile):
        score_percentage = round(len(good_pile) * 100 / len(bad_pile + good_pile), 1)
        self.audio.speak("Testing is done. You got " + str(score_percentage) + " percent right.")

        if score_percentage != 100:
            self.audio.speak("Would you like to go through letters you got wrong?")
            if self.audio.recognize_speech(app=self)["transcription"].find('yes') != -1:
                self.audio.speak("Okay, let's go through the characters you answered wrong. You can move on to the next character by saying next.")
                for c in bad_pile:
                    self.print_character_all_cells(c)
                    self.audio.speak("This is " + character_dict[c]['pronunciation'])
                    self.wait_for_audio("next")
                self.audio.speak("That were all the characters you answered wrong.")
        else:
            self.audio.speak("Well done!")

        self.audio.speak("Do you want to take another test?")
        if self.audio.recognize_speech()["transcription"].find('yes') != -1:
            self.run_test()

        self.on_quit()

    def characters_shuffled(self, test_length='short'):
        chars = (
            [(char, 'alphabet') for char in alphabet_dict] +
            [(char, 'punctuation') for char in punctuation_dict] +
            [(char, 'indicator') for char in indicator_dict] +
            [(char, 'digit') for char in digit_dict]
        )

        test_lengths = {
            'short': 10,
            'medium': 20,
            'full': len(chars)
        }

        chars_shuffled = random.sample(chars, test_lengths[test_length])
        return chars_shuffled
