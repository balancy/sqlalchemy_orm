from bs4 import BeautifulSoup
import requests


def fetch_posts_from_habr():
    url = "https://habr.com/ru/news/"
    response = requests.get(url)
    response.raise_for_status()

    parsed_html = BeautifulSoup(response.text, "lxml")
    all_html_news = parsed_html.select(".posts_list .post")

    news_set = []
    for post in all_html_news:
        news_set.append({
            "title": post.select_one(".post__title a").text,
            "text": post.select_one(".post__text").text.strip(),
            "username": post.select_one(".post__meta .user-info").text.strip(),
            "tags": [elm.text for elm in post.select(
                ".post__hubs .inline-list__item_hub a"
            )]
        })

    return news_set
