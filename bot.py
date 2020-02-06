from misc import TOKEN, STORES
from dialog_flow_bot import text_message

import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from geopy.distance import distance


bot = telebot.TeleBot(TOKEN)

# Создание основного меню
main_buttons = {
    'addresses': KeyboardButton('Адреса магазинов', request_location=True),
    'payment': KeyboardButton('Способы оплаты'),
    'delivery': KeyboardButton('Способы доставки')
}

main_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_menu.add(main_buttons['addresses'], main_buttons['payment'], main_buttons['delivery'])

# Создание инлайн-меню
others_stores_button = InlineKeyboardButton(text='Другие магазины...', callback_data='stores')

others_stores_inline_menu = InlineKeyboardMarkup()
others_stores_inline_menu.add(others_stores_button)


# Действия по команде /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
    bot.reply_to(message, f'Привет , {message.from_user.first_name}, я бот интернет-магазина.',
                 reply_markup=main_menu)


# Ищем ближайший к пользователю магазин
@bot.message_handler(content_types=['location'], func=lambda message: True)
def store_location(message: Message):
    user_lon = message.location.longitude
    user_lat = message.location.latitude
    sorted_distances = get_distances(user_lat, user_lon)
    bot.send_message(
        message.chat.id,
        f'{message.from_user.first_name}, '
        f'ближайший к Вам магазин {sorted_distances[0][0]} находится от Вас на расстоянии '
        f'{round(sorted_distances[0][1][0], 3)} км'
        f' по адресу:\n {sorted_distances[0][1][1]}',
        reply_markup=others_stores_inline_menu
    )


#  Обработка нажатия кнопок основного меню
@bot.message_handler(content_types=['text'], func=lambda message: True)
@bot.edited_message_handler(content_types=['text'])
def echo_all(message: Message):
    if message.text == 'Способы доставки':
        bot.reply_to(message,
                     f'{message.from_user.first_name}, Мы доставляем товары следующими способами: \n'
                     f'Самовывоз\n'
                     f'Укрпошта\n'
                     f'Нова пошта',
                     reply_markup=main_menu)
    elif message.text == 'Способы оплаты':
        bot.reply_to(message,
                     f'{message.from_user.first_name}, Мы принимаем следующие способы оплаты:\n'
                     f'Наличные\n'
                     f'Банковский перевод\n',
                     reply_markup=main_menu)
    else:
        bot.reply_to(message, f'{message.from_user.first_name}, {text_message(message.text)}',
                     reply_markup=main_menu)


@bot.callback_query_handler(func=lambda message: True)
def callback_others_stores(call):
    if call.data == 'stores':
        bot.send_message(call.message.chat.id, text=f'{[store["title"] for store in STORES]}')


# Получаем отсортированный список с расстояниями от пользователя до всех магазинов в списке.
# Список имеет вид [('Название магазина', (расстояние до пользователя, адрес))]
def get_distances(user_lat, user_lon):
    distances = {}

    for store in STORES:
        distances[store['title']] = (
            distance((user_lat, user_lon), (store['lat'], store['lon'])).kilometers,
            store['address']
        )

    list_distances = list(distances.items())
    sorted_distances = sorted(list_distances, key=lambda x: x[1][0])
    return sorted_distances


def main():
    # запускаем бота
    bot.polling(timeout=60)


if __name__ == '__main__':
    main()
