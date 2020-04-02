from app import App
from arduino import Arduino
from cell import Cell
from audio import Audio
import feedparser

class Headlines(App):

    categories = {
        # A dictionary so that the speech input is convertable to the string needed fot the URL
        # I.e the URL includdes "uk_politics", this lets the user say just "politics"
        "front page": "front_page", "business": "business",
        "entertainment": "entertainment", "health": "health",
        "education":"education", "politics":"uk_politics",
        "england":"england", "scotland":"scotland",
        "wales":"wales", "tech":"technology",
        "world":"world"
    }

    def show_headlines(self, category, ptr):
        self.audio.speak("We are fetching the articles.")
        article_ptr = ptr
        options = ["next","back","more","again","home"]
        #Get RSS feed given catagory
        feed = feedparser.parse("http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/"+category+"/rss.xml")

        article_list = feed.entries

        show = True
        while True:
            if show:
                self.print_text(article_list[article_ptr].title)
            response = self.await_response(options)
            if response == "next":
                if article_ptr + 1 > len(article_list):
                    self.audio.speak("You have reached the end of the articles in this category.")
                    show = False
                else:
                    article_ptr += 1
                    show = True

            elif response == "back":
                if article_ptr - 1 < 0:
                    self.audio.speak("There are no previous articles")
                    show = False
                else:
                    article_ptr -= 1
                    show = True

            elif response == "more":
                self.print_text(article_list[article_ptr].summary)
                #print(article_list[article_ptr].summary)
                show = False

            elif response == "again":
                show = True
            elif response == "home":
                self.main()

    def get_category_response(self, prompt, extended_prompt):
        #First time it is called, it shows the extended_prompt
        options = [c for c in self.categories]

        self.audio.speak(prompt)
        if self.first_attempt:
            self.audio.speak(extended_prompt)
            self.first_attempt = False            

        response = self.await_response(options)
        return response

    def main(self):
        category = self.get_category_response("Which category would you like to read? ", "Whenever you want to hear your options say \"options\". ")
        self.show_headlines(self.categories[category], 0)

    def on_start(self):
        self.instruction = """
            Welcome to Headlines.
            This will allow you to read the news in braille!
            Say 'next' or 'back' to go to the next or the previous article,
            'more' if you would like to read more,
            'again' to read the headline again
            and 'home' to return to the beginning.
        """
        self.first_attempt = True
        self.main()
