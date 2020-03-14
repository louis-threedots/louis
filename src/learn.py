from app import App
from characters import *

class Learn(App):

    def on_start(self):
        # instruction when app started, skip when the user says skip
        self.app_instruction("Here you will learn the alphabet. You can move on to the next character by saying next.")
        self.learn_category()

    def learn_category(self):
        self.audio.speak("""
            Which of the following categories would you like to learn?
            The alphabet, punctuation, digits, special indicators or contractions?
        """)

        reply = self.audio.recognize_speech(app=self)["transcription"]
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
        else:
            self.audio.speak("I did not understand.")
            self.learn_category() # ask the question again
            return

        for c in learn_chars:
            self.print_character_all_cells(c)
            self.audio.speak(audio_announcement + ' ' + character_dict[c]['pronunciation'])
            self.audio.await_response(["next"])

        self.audio.speak("That were all the characters. Would you like to learn another category?")
        if self.audio.recognize_speech()["transcription"].find('yes') != -1:
            self.learn_category()

        self.on_quit()
