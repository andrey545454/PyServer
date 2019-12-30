from newsapi import NewsApiClient
import configparser
import json
import datetime
"""
Powered by News API
"""

if __name__ == "__main__":
    # Чтение api ключа из конфиг файла
    config = configparser.ConfigParser()
    config.read("config.ini")
    api_key = config["news_api"]["api_key"]

    key_word = input()

    news_api_client = NewsApiClient(api_key=api_key)

    # Получаем последние новости из категории business
    top_ru_news = news_api_client.get_top_headlines(
        country="ru",
        category="business",
        page_size=100
    )
    top_us_news = news_api_client.get_top_headlines(
        country="us",
        category="business",
        page_size=100
    )
    # Берём новости сегодняшней даты
    today_business_news = list(filter(
        lambda article:
        datetime.datetime.strptime(article["publishedAt"],"%Y-%m-%dT%H:%M:%SZ").day == datetime.datetime.today().day,
        top_ru_news["articles"]+top_us_news["articles"]
    ))

    today_business_news.sort(
        key=lambda article:
            article["title"].lower().count(key_word.lower()) if article["title"] is not None else 0
            +
            article["content"].lower().count(key_word.lower()) if article["content"] is not None else 0,
        reverse=True
    )
    # Запись в файл
    with open("news.json", 'w') as file:
        json.dump(today_business_news, file, indent=2)


