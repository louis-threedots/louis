from app import App
from characters import *

class Learn(App):

    def on_start(self):
        self.instruction = """
            Welcome to Learn.
            Here you will learn the alphabet.
            You can move on to the next character by saying next.
        """
        self.learn_category()

    def learn_category(self):
        self.audio.speak("Which of the following categories would you like to learn? The alphabet, punctuation, digits, special indicators or contractions?")

        reply = self.await_response(["alphabet", "punctuation", "digits", "contractions", "indicators"])
        if "alphabet" in reply:
            self.audio.speak("Let's learn the lowercase alphabet.")
            learn_chars = alphabet_dict
            audio_announcement = "This is the letter"
        elif "punctuation" in reply:
            self.audio.speak("Let's learn punctuation characters.")
            learn_chars = punctuation_dict
            audio_announcement = "This is a"
        elif "digits" in reply:
            self.audio.speak("Let's learn digits.")
            learn_chars = digit_dict
            audio_announcement = "This is the number"
        elif "contractions" in reply:
            self.audio.speak("Let's learn contractions.")
            learn_chars = contraction_dict
            audio_announcement = "This is the contraction"
        elif "indicators" in reply:
            self.audio.speak("Let's learn special indicators.")
            learn_chars = indicator_dict
            audio_announcement = "This announces a"

        for c in learn_chars:
            self.print_character_all_cells(c)
            self.audio.speak(audio_announcement)
            self.audio.speak(character_dict[c]['pronunciation'])
            self.await_response(["next"])

        self.audio.speak("That were all the characters. Would you like to learn another category?")
        reply = self.await_response(["yes","no"])
        if reply == 'yes':
            self.learn_category()

        self.on_quit()
