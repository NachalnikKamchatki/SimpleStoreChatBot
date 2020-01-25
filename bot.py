from misc import token
import requests

# https://api.telegram.org/bot<token>/METHOD_NAME

URL = f'https://api.telegram.org/bot{token}'


def get_me():
    url = f'{URL}/getMe'
    r = requests.get(url)
    return r.json()


def get_last_updates():
    url = f'{URL}/getUpdates'
    r = requests.get(url)
    return r.json()['result'][-1]


def main():
    print(get_last_updates())


if __name__ == '__main__':
    main()
