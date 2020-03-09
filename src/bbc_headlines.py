import feedparser

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

#List of alternative words to yes or quit, might be useful if this is in the main app class?
stopping_words = ["stop", "exit", "quit", "leave", "done"]
yes_words = ["yes", "yeah", "please","yep"]

#Lets the user know their options at any given time. I think this would be a good feature in all apps.
def show_options(options):
        for o in options:
            #Would be good to listen while reading these to see if user wants to stop
            print(o)

def show_headlines(category, ptr):

    article_ptr = ptr

    options = ["next","back","more","again","home","quit"]
    instructions = "Say \"next\" or \"back\" to go to the next or the previous article, \"more\" if you would like to read more, \"again\" to read the headline again and \"home\" to return to the beginning."
    #Get RSS feed given catagory
    feed = feedparser.parse("http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/"+category+"/rss.xml")

    article_list = feed.entries

    show = True
    #Is there a way to quit while it is outputting?
    while True:
        if show == True:
            print(article_list[article_ptr].title)

        #Listen should work while the output is changing so user can skip article.
        listen = input()

        if listen == "next":
            if article_ptr + 1 > len(article_list):
                print("You have reached the end of the articles in this category.")
                show = False
            else:
                article_ptr += 1
                show = True

        elif listen == "back":
            if article_ptr - 1 < 0:
                print("There are no previous articles")
                show = False
            else:
                article_ptr -= 1
                show = True

        elif listen in stopping_words:
            quit()

        elif listen == "more":
            print(article_list[article_ptr].summary)
            show = False

        elif listen == "again":
            show = True

        elif listen == "options":
            show_options(options)
            show = False

        elif listen == "home":
            main()

        else:
            print("Invalid input, try again.")
            show = False

def quit():
    options = ['yes','no']
    while True:
        inp = input("Would you like to read more from another category? ")
        if inp in yes_words:
            main()
        elif inp == "options":
            show_options(options)
        else:
            print("Exiting...")
            raise SystemExit

def hard_quit():
    print("Exiting...")
    raise SystemExit

def get_category_response(prompt, extended_prompt):
    #First time it is called, it shows the extended_prompt
    options = [c for c in categories]
    options.append("quit")

    first_attempt = True
    while True:
        try:
            if first_attempt == True:
                out = prompt + extended_prompt
                first_attempt = False
            else:
                out = prompt

            inp = input(out)
        except:
            print("I'm sorry I didn't understand that.")

        if inp == "options":
            show_options(options)

        elif inp in stopping_words:
            hard_quit()

        elif inp not in categories:
            print("Non-valid category, please try again.")
            continue

        else:
            return inp

def main():
    category = get_category_response("Which category? ", "Whenever you want to hear your options say \"options\". ")
    show_headlines(categories[category], 0)

print("Welcome to the BBC headlines app. This will allow you to read the news in braille!")
main()
