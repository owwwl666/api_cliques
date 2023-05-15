# Описание
Проект реализован на основе получения доступа к API [bit.ly](https://bitly.com) и создании консольной утилиты, сокращающей ссылку, а также подсчета количества переходов по ней
# Требования к окружению
- Операционная система: `Linux Mint`
- Необходимые пакеты и их версии указаны в `requirements.txt`.
# Настройка окружения
При реализции в скрипт были добавлены закрытые данные, в нашем случае, токен. Он служит для того, чтобы обращаться по нему, как по ключу к функционалу нашего профиля на [bit.ly](https://bitly.com):
- Мы добавили его в файл `.env`, предварительно установив модуль [python-dotenv](https://pypi.org/project/python-dotenv/)
- В `.env` указали ключ-значение
  `TOKEN_BITLY=e62f9766890632d27a4c4d300432cc2a9928b8be`
- Импортируем в скрипте `cliques.py`
  ```
  import os
  from dotenv import load_dotenv
  load_dotenv()
  TOKEN_BITLY = {'Authorization': f'Bearer {os.environ["TOKEN_BITLY"]}'}
  ```
 - Изменить значение токена по ключу:
  `os.environ["TOKEN_BITLY"] = "NEW VALUE"`
  # Реализация проекта
  Реализация в файле `cliques.py`. Все необходимые операции с URL, которые проводились в скрипте, описаны в [документации](https://gist.github.com/dvmn-tasks/58f5fdf7b8eb61ea4ed1b528b74d1ab5#GetClicks)
  - `pip install NamePackege` -> установка необходимых пакетов из `requirements.txt`.
  - Импорт библиотек
    ```
    import os
    from dotenv import load_dotenv
    import requests
    from urllib.parse import urlparse
    ```
 - Объявление функций для реализации логики скрипта.
    ```
    def shorten_link(token, href):
    """Сокращение ссылки"""
      ...
    ```
    ```
    def count_clicks(url_count_clincks, token):
    """Количество кликов по ссылке"""
      ...
    ```
    ```
    def is_bitlink(url_is_bitlink, token):
     """Проверка ссылки на сокращенность"""
      ...
    ```
    ```
    def main():
      load_dotenv()

      href = input('Введите ссылку:')
      href_without_http = urlparse(href)._replace(scheme="").geturl() #убираем название протокала из ссылки

      TOKEN_BITLY = {'Authorization': f'Bearer {os.environ["TOKEN_BITLY"]}'} # объявляем токен для доступа к API bitly

      url_count_clincks = f'https://api-ssl.bitly.com/v4/bitlinks/{href_without_http}/clicks/summary' # полная ссылка для подсчета переходов по сслылке
      url_is_bitlink = f'https://api-ssl.bitly.com/v4/bitlinks/{href_without_http}'# полная ссылка для сокращения адреса url
      
      if is_bitlink(url_is_bitlink, TOKEN_BITLY): # если ссылка уже сокращенная, то возвращаем количество переходов по ней
        clicks_count = count_clicks(url_count_clincks, TOKEN_BITLY)
        return f'Количетво кликов: {clicks_count}'
      try: # пытаемся сократить сслыку
        bitlink = shorten_link(TOKEN_BITLY, href)
        return f'Битлинк: {bitlink}'
      except requests.exceptions.HTTPError: # возбуждаем исключение
        raise 'Некорректная ссылка'
      
    ```
    # Результаты
    ![](https://dvmn.org/filer/canonical/1610994077/769/)
