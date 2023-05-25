# Описание

Проект реализован на основе получения доступа к API [bit.ly](https://bitly.com) и создании консольной утилиты, сокращающей ссылку, а также подсчета количества переходов по ней

# Установка зависимостей

Необходимые пакеты и их версии указаны в `requirements.txt`.
Установка всех необходимых зависимостей:

`pip install -r requirements.txt`
    
# Требования к окружению

Операционная система `Linux`

# Настройка окружения

При реализции в скрипт были добавлены закрытые данные, в нашем случае, токен. Он служит для того, чтобы обращаться по нему, как по ключу к функционалу нашего профиля на [bit.ly](https://bitly.com):
- Мы добавили его в файл `.env`, предварительно установив модуль [python-dotenv](https://pypi.org/project/python-dotenv/)
- В `.env` указали ключ-значение
  `BITLY_TOKEN=e62f9766890632d27a4c4d300432cc2a9928b8be`
- Импортируем в скрипте `main.py`

  ```python
  import os
  from dotenv import load_dotenv
  load_dotenv()
  BITLY_TOKEN = {'Authorization': f'Bearer {os.environ["BITLY_TOKEN"]}'}
  ```
 - Изменить значение токена по ключу:
  `os.environ["BITLY_TOKEN"] = "NEW VALUE"`
  # Реализация проекта
  Реализация в файле `main.py`. Заметим,что мы не вводили ссылку в консоль с помощью функции `input()` для дальнейшего ее преобразования, а передавали ее как позиционный аргумент в командную строку, используя стандартную библиотеку [argparse](https://slides.dvmn.org/argparse/#/) .Все необходимые операции с URL, которые проводились в скрипте, описаны в [документации](https://gist.github.com/dvmn-tasks/58f5fdf7b8eb61ea4ed1b528b74d1ab5#GetClicks)
  - Импорт библиотек
  
    ```python
    import os
    import argparse
    from dotenv import load_dotenv
    import requests
    from urllib.parse import urlparse
    ```
 - Объявление функций для реализации логики скрипта.
 
    ```python
    def shorten_link(token, href):
    """Сокращение ссылки"""
      ...
    ```
    ```python
    def count_clicks(url_count_clincks, token):
    """Количество кликов по ссылке"""
      ...
    ```
    ```python
    def is_bitlink(url_is_bitlink, token):
     """Проверка ссылки на сокращенность"""
      ...
    ```
    ```python
    def main():
      load_dotenv()

      parser = argparse.ArgumentParser()
      parser.add_argument('link_for_bitly')
      args = parser.parse_args()

      href = args.link_for_bitly
      href_without_http = urlparse(href)._replace(scheme="").geturl()

      request_header = {'Authorization': f'Bearer {os.environ["TOKEN_BITLY"]}'}

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
    ```
    # Результаты
    ![](https://dvmn.org/media/Screenshot_from_2018-10-31_15-00-02.png)
