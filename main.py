import telebot

bot = telebot.TeleBot('6150776858:AAFgMzCcTuLUDnEoO8RNS2HMpNkH5xaf22Q')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Выбери, что ты хочешь сделать:',
                     reply_markup=main_keyboard())


def main_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_task = telebot.types.KeyboardButton("Выдача задания")
    btn_time = telebot.types.KeyboardButton("Регулировка времени генерации")
    markup.add(btn_task, btn_time)
    return markup


bot.polling(none_stop=True)
