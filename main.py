import os
import argparse
from dotenv import load_dotenv
import requests
from urllib.parse import urlparse


def shorten_link(request_header, href):
    """Сокращение ссылки"""
    url_shorten_link = 'https://api-ssl.bitly.com/v4/shorten'
    body = {
        "long_url": href,
    }
    response = requests.post(url_shorten_link, json=body,
                             headers=request_header)
    response.raise_for_status()
    return response.json()['id']


def count_clicks(url_count_clincks, request_header):
    """Количество кликов по ссылке"""
    response = requests.get(url_count_clincks, headers=request_header)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(url_is_bitlink, request_header):
    """Проверка ссылки на сокращенность"""
    response = requests.get(url_is_bitlink, headers=request_header)
    return response.ok


def main():
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument('link_for_bitly')
    args = parser.parse_args()

    href = args.link_for_bitly
    url_parse = urlparse(href)
    href_without_http = url_parse.netloc + url_parse.path

    request_header = {'Authorization': f'Bearer {os.environ["BITLY_TOKEN"]}'}

    url_count_clincks = f'https://api-ssl.bitly.com/v4/bitlinks/{href_without_http}/clicks/summary'
    url_is_bitlink = f'https://api-ssl.bitly.com/v4/bitlinks/{href_without_http}'

    if is_bitlink(url_is_bitlink, request_header):
        clicks_count = count_clicks(url_count_clincks, request_header)
        return f'Количетво кликов: {clicks_count}'
    try:
        bitlink = shorten_link(request_header, href)
        return f'Битлинк: {bitlink}'
    except requests.exceptions.HTTPError:
        raise 'Некорректная ссылка'


if __name__ == '__main__':
    print(main())
