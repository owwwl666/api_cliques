import os
from dotenv import load_dotenv
import requests
from urllib.parse import urlparse


def shorten_link(token, href):
    """Сокращение ссылки"""
    url_shorten_link = 'https://api-ssl.bitly.com/v4/shorten'
    body = {
        "long_url": href,
    }
    response = requests.post(url_shorten_link, json=body,
                             headers=token)
    response.raise_for_status()
    return response.json()['id']


def count_clicks(url_count_clincks, token):
    """Количество кликов по ссылке"""
    response = requests.get(url_count_clincks, headers=token)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(url_is_bitlink, token):
    """Проверка ссылки на сокращенность"""
    response = requests.get(url_is_bitlink, headers=token)
    return response.ok


def main():
    load_dotenv()

    href = input('Введите ссылку:')
    href_without_http = urlparse(href)._replace(scheme="").geturl()

    TOKEN_BITLY = {'Authorization': f'Bearer {os.environ["TOKEN_BITLY"]}'}

    url_count_clincks = f'https://api-ssl.bitly.com/v4/bitlinks/{href_without_http}/clicks/summary'
    url_is_bitlink = f'https://api-ssl.bitly.com/v4/bitlinks/{href_without_http}'

    if is_bitlink(url_is_bitlink, TOKEN_BITLY):
        clicks_count = count_clicks(url_count_clincks, TOKEN_BITLY)
        return f'Количетво кликов: {clicks_count}'
    try:
        bitlink = shorten_link(TOKEN_BITLY, href)
        return f'Битлинк: {bitlink}'
    except requests.exceptions.HTTPError:
        raise 'Некорректная ссылка'


if __name__ == '__main__':
    print(main())
