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

    news_api_client = NewsApiClient(api_key=api_key)

    # Получаем последние новости из категории business
    top_news = news_api_client.get_top_headlines(
        category="business",
        page_size=100
    )
    # Берём новости сегодняшней даты
    today_business_news = list(filter(
        lambda article:
        datetime.datetime.strptime(article["publishedAt"],"%Y-%m-%dT%H:%M:%SZ").day == datetime.datetime.today().day,
        top_news["articles"]
    ))
    # Запись в файл
    with open("news.json", 'w') as file:
        json.dump(today_business_news, file, indent=2)


