import json
from apiai import ApiAI
from misc import DIALOG_FLOW_TOKEN


def text_message(s: str):
    req = ApiAI(DIALOG_FLOW_TOKEN).text_request()
    req.lang = 'ru'
    req.session_id = 'store_bot'
    req.query = s
    resp_json = json.loads(req.getresponse().read().decode('utf-8'))
    response = resp_json['result']['fulfillment']['speech']
    if response:
        return response
    else:
        return 'Я тебя не понимаю. Спроси что-нибудь еще.'


def main():
    while True:
        s = input('Введите ваше сообщение: ')
        if s == 'выход':
            break
        print(text_message(s))


if __name__ == '__main__':
    main()
