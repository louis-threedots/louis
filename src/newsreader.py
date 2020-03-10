import requests
from bs4 import BeautifulSoup

def take_news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    section = soup.find("meta", property="article:section", content=True)
    title = soup.find("meta", property="og:title", content=True)
    if section and title:
        print(title["content"] + "," + section["content"], url)
def main():
    take_news("https://www.bbc.co.uk/news/uk")

if __name__ == '__main__':
    main()