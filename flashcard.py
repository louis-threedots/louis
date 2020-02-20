from src.audio import Audio
import string
import random
import time

def play_flashcard():

    #todo: app should stop whenever the user says "stop application"
    while take_answer() != "stop application":
        audio = Audio()
        alphabet = list(string.ascii_lowercase)
        alphabet_shuffled = random.shuffle(alphabet, random)

        # instruction when app started
        # skip when the user says skip
        app_instruction()

        #initialise good_pile and bad_pile
        good_pile = []
        bad_pile = []
        audio.start_background_listening()

        for c in alphabet_shuffled:
            #initialise variables for each question
            chances = 3
            correct = False
            score = 0

            # todo: display each character on a cell
            # display_on_cell(c)
            audio.speak('Which letter is this? You have 10 seconds to answer.')
            time.sleep(10)
            while correct == False or chances > 0:
                if take_answer() == c:
                    audio.speak('correct answer! Move on to next question.')
                    good_pile.append(c)
                    score += score
                    correct = True
                elif take_answer() != c:
                    chances -= chances
                    if chances == 0:
                        audio.speak("You have used all your chances to answer. The correct answer is "+c)
                        audio.speak("I will save this character for later.")
                        bad_pile.append(c)
                        audio.speak("Moving on to next question.")
                        break
                    if chances > 0:
                        audio.speak('Incorrect! you have '+chances+" more chances to respond")

        test_done_instruction(bad_pile, score)


def app_instruction():
    instruction = "Welcome to the Flashcard App. The purpose of this application is to test how much have you learnt from Learn. Let's start testing."
    audio = Audio()
    audio.speak("Would you like to listen to an instruction for this application?")

    #take answer from the user
    if take_answer() == 'yes':
        audio.speak(instruction)
    elif take_answer() == 'no':
        audio.speak("skipping instruction")
    elif take_answer() != 'yes' or take_answer() != 'no':
        audio.speak("Wrong answer. Please respond again.")

def test_done_instruction(bad_pile, score):

    audio = Audio()
    audio.speak("Testing is done. You got"+round(score*100/26, 1)+" percent right. Would you like to go through letters you got wrong?")
    if take_answer() == "yes":
        audio.speak("Okay, lets go through the characters you answered wrong.")
        while take_answer() != "stop application":
            for c in bad_pile:
                audio.speak("This is "+c)
                # todo: physically display letter c
                time.sleep(10)

    elif take_answer() == "no":
        audio.speak("Would you like to exit Flashcard?")
        if take_answer() == "yes":
            exit_flashcard
        elif take_answer() == "no":
            audio.speak("do you want to take a test again?")
            if take_answer() == "yes":
                play_flashcard()
            elif take_answer() == "no":
                exit_flashcard()

def take_answer():
    audio = Audio()
    while audio.recognize_speech()["transcription"] is not None:
        answer = audio.recognize_speech()["transcription"]
        break
    return answer

def exit_flashcard():
    audio = Audio()
    audio.speak("Turning off Flashcard")
    audio.start_background_listening()
    #todo: switch to waiting mode / ready to open other applications
