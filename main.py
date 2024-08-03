import requests
from urllib.parse import urlparse
import os
import argparse


def shorten_link(token, long_url):
    url = "https://api-ssl.bitly.com/v4/shorten"
    headers = {"Authorization": "Bearer {}".format(token)}
    params = {"long_url": long_url}
    response = requests.post(url, headers=headers, json=params)
    response.raise_for_status()
    return response.json()["id"]


def count_clicks(token, link):
    url = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary".format(
        link)
    headers = {"Authorization": "Bearer {}".format(token)}
    params = {"unit": "month", "units": "-1"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(bitlink, token):
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"
    headers = {"Authorization": "Bearer {}".format(token)}
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    token = os.environ['BITLY_TOKEN']
    parser = argparse.ArgumentParser(
        description='Описание что делает программа'
    )
    parser.add_argument('--url', help='Введите ссылку ')
    args = parser.parse_args()
    parsed_url = urlparse(args.url)
    parsed_url = f"{parsed_url.netloc}{parsed_url.path}"
    try:
        if is_bitlink(parsed_url, token):
            print("Количество кликов: ", count_clicks(token, parsed_url))
        else:
            print("Битлинк: ", shorten_link(token, args.url))
    except requests.exceptions.HTTPError:
        print("Вы ввели неправильную ссылку или неверный токен.")


if __name__ == "__main__":
    main()
