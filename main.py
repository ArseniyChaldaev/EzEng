import telebot
from telebot import types

TOKEN = '6150776858:AAFgMzCcTuLUDnEoO8RNS2HMpNkH5xaf22Q'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    btn_give_task = types.KeyboardButton("📚give me a task")
    btn_time_change = types.KeyboardButton("⌚️change the generation time")

    markup.add(btn_give_task, btn_time_change)

    bot.send_message(message.chat.id, 'Hi, {0.first_name}! Choose what you want to do:'.format(message.from_user),
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '📚give me a task':

            markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

            btn_task_type_1 = types.KeyboardButton('📕Translation')
            btn_task_type_2 = types.KeyboardButton('📗Determination of tenses')
            btn_task_type_3 = types.KeyboardButton('📘Insert the correct word')
            btn_back = types.KeyboardButton('⬅️Back')

            markup.add(btn_task_type_1, btn_task_type_2, btn_task_type_3, btn_back)

            bot.send_message(message.chat.id,
                             'Choose a type:'.format(message.from_user),
                             reply_markup=markup)

        elif message.text == '⌚️change the generation time':
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

            btn_time_type_1 = types.KeyboardButton('🕛10:00')
            btn_time_type_2 = types.KeyboardButton('🕗20:00')
            btn_back = types.KeyboardButton('⬅️Back')

            markup.add(btn_time_type_1, btn_time_type_2, btn_back)

            bot.send_message(message.chat.id,
                             'Choose the right time:'.format(message.from_user),
                             reply_markup=markup)
        if message.text == '📕Translation' or message.text == '📗Determination of tenses' or message.text == '📘Insert the correct word':
            markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

            btn_difficulty_easy = types.KeyboardButton("🟢easy")
            btn_difficulty_medium = types.KeyboardButton("🟡medium")
            btn_difficulty_hurd = types.KeyboardButton("🔴hurd")
            btn_back = types.KeyboardButton('⬅️Back')

            markup.add(btn_difficulty_easy, btn_difficulty_medium, btn_difficulty_hurd, btn_back)

            bot.send_message(message.chat.id,
                             '{0.first_name}, choose the difficulty:'.format(message.from_user),
                             reply_markup=markup)

        elif message.text == '⬅️Back' or message.text == '🕛10:00' or message.text == '🕗20:00':
            if message.text == '🕛10:00' or message.text == '🕗20:00':
                bot.send_message(message.chat.id, 'The time is setted.')
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

            btn_give_task = types.KeyboardButton("📚give me a task")
            btn_time_change = types.KeyboardButton("⌚️change the generation time")

            markup.add(btn_give_task, btn_time_change)

            bot.send_message(message.chat.id,
                             '{0.first_name}, choose what you want to do:'.format(message.from_user),
                             reply_markup=markup)


bot.polling(none_stop=True)
