import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

href = input('Введите ссылку:')


def shorten_link(url_shorten_link, token, href):
    """Сокращение ссылки"""
    body = {
        "long_url": href,
    }
    response = requests.post(url_shorten_link, json=body,
                             headers=token)
    response.raise_for_status()
    return response.json()['id']


def count_clicks(url_count_clincks, token, sum_clicks=0):
    """Количество кликов по ссылке"""
    response = requests.get(url_count_clincks, headers=token)
    response.raise_for_status()
    clicks = response.json()['link_clicks']
    for click in clicks:
        sum_clicks += click['clicks']
    return sum_clicks


def is_bitlink(url_is_bitlink, url_shorten_link, url_count_clincks, token):
    """Проверка ссылки на сокращенность"""
    response = requests.get(url_is_bitlink, headers=token)
    if response.ok:
        clicks_count = count_clicks(url_count_clincks, token)
        return f'Количетво кликов: {clicks_count}'
    try:
        bitlink = shorten_link(url_shorten_link, token, href)
        return f'Битлинк: {bitlink}'
    except requests.exceptions.HTTPError:
        raise 'Некорректная ссылка'


def main():
    token = {'Authorization': f'Bearer {os.environ["TOKEN"]}'}
    href_without_http = urlparse(href)._replace(scheme="").geturl()
    url_shorten_link = 'https://api-ssl.bitly.com/v4/shorten'
    url_count_clincks = f'https://api-ssl.bitly.com/v4/bitlinks/{href_without_http}/clicks'
    url_is_bitlink = f'https://api-ssl.bitly.com/v4/bitlinks/{href_without_http}'
    pprint(is_bitlink(url_is_bitlink, url_shorten_link, url_count_clincks, token))


if __name__ == '__main__':
    main()
