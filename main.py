from datetime import datetime
from threading import Thread

import telebot
from apscheduler.schedulers.blocking import BlockingScheduler
from telebot import types, custom_filters
from telebot.apihelper import ApiTelegramException
from telebot.handler_backends import StatesGroup, State
from telebot.storage import StateMemoryStorage

from api.rapid_api import RapidApi
from constants import *
from data.db_helper import Database

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(TELEGRAM_TOKEN, state_storage=state_storage)

scheduler = BlockingScheduler(timezone="Europe/Moscow")

db: Database = Database()
translate_api = RapidApi()


# States group.
class BotStates(StatesGroup):
    main_menu = State()
    task_menu = State()
    task_difficult_menu = State()
    task_check_answer = State()
    schedule_menu = State()
    schedule_set = State()


@bot.message_handler(commands=['start'])
def start(message):
    db.save_user(message.chat)
    show_main_menu(message)


def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_give_task = types.KeyboardButton("📚Give me a task")
    btn_time_change = types.KeyboardButton("⌚️Change the generation time")
    markup.add(btn_give_task, btn_time_change)
    bot.set_state(message.from_user.id, BotStates.main_menu, message.chat.id)
    bot.send_message(message.chat.id, 'Hi, {0.first_name}! Choose what you want to do:'.format(message.from_user),
                     reply_markup=markup)


@bot.message_handler(state=BotStates.main_menu)
def main_menu_handler(message):
    if message.text == '📚Give me a task':
        show_task_menu(message)
    elif message.text == '⌚️Change the generation time':
        show_schedule_menu(message)


def show_schedule_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_time_type_1 = types.KeyboardButton('🕛10:00')
    btn_time_type_2 = types.KeyboardButton('🕗20:00')
    btn_back = types.KeyboardButton('⬅️Back')
    markup.add(btn_time_type_1, btn_time_type_2, btn_back)
    bot.set_state(message.from_user.id, BotStates.schedule_menu, message.chat.id)
    bot.send_message(message.chat.id,
                     'Choose the right time:'.format(message.from_user),
                     reply_markup=markup)


def show_task_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for theme in THEMES.keys():
        markup.add(types.KeyboardButton(theme))
    markup.add(types.KeyboardButton('⬅️Back'))
    bot.set_state(message.from_user.id, BotStates.task_menu, message.chat.id)
    bot.send_message(message.chat.id,
                     'Choose a type:'.format(message.from_user),
                     reply_markup=markup)


@bot.message_handler(state=BotStates.task_menu)
def task_menu_handler(message):
    if message.text in THEMES:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['theme'] = THEMES[message.text]
        show_difficult_menu(message)
    elif message.text == '⬅️Back':
        show_main_menu(message)


def show_difficult_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    buttons = []
    for difficulty in DIFFICULTIES.keys():
        buttons.append(types.KeyboardButton(difficulty))
    markup.add(*buttons)
    markup.add(types.KeyboardButton('⬅️Back'))
    bot.set_state(message.from_user.id, BotStates.task_difficult_menu, message.chat.id)
    bot.send_message(message.chat.id,
                     '{0.first_name}, choose the difficulty:'.format(message.from_user),
                     reply_markup=markup)


@bot.message_handler(state=BotStates.task_difficult_menu)
def task_difficult_menu_handler(message):
    if message.text in DIFFICULTIES:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            task = db.get_task(message.chat.id, data['theme'], DIFFICULTIES[message.text])
            db.save_user_task(message.from_user.id, task.id)
            data['answer'] = task.answer.lower()
            show_answer_menu(message, task.text)
    elif message.text == '⬅️Back':
        show_task_menu(message)


def show_answer_menu(message, text):
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    markup.add(types.KeyboardButton('⬅️Back'))
    bot.set_state(message.from_user.id, BotStates.task_check_answer, message.chat.id)
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(state=BotStates.task_check_answer)
def task_check_answer_handler(message):
    if message.text != '⬅️Back':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if message.text.lower() == data['answer']:
                bot.send_message(message.chat.id, 'Right!!!')
            else:
                bot.send_message(message.chat.id, f"Wrong!!! Answer: {data['answer']}")
    show_main_menu(message)


@bot.message_handler(state=BotStates.schedule_menu)
def schedule_menu_handler(message):
    if message.text == '⌚️Change the generation time':
        show_schedule_menu(message)
    elif message.text == '⬅️Back':
        start(message)


def show_schedule_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    buttons = []
    for time in TIMES.keys():
        buttons.append(types.KeyboardButton(time))
    markup.add(*buttons)
    markup.add(types.KeyboardButton('⬅️Back'))
    bot.set_state(message.from_user.id, BotStates.schedule_set, message.chat.id)
    bot.send_message(message.chat.id,
                     'Choose the right time:'.format(message.from_user),
                     reply_markup=markup)


@bot.message_handler(state=BotStates.schedule_set)
def schedule_set_handler(message):
    if message.text != '⬅️Back':
        if message.text in TIMES.keys():
            db.save_schedule(message.chat.id, TIMES[message.text])
            bot.send_message(message.chat.id, "Time is set")
        else:
            bot.send_message(message.chat.id, 'Wrong time')
            return
    show_main_menu(message)


def send_words_job():
    hour = datetime.today().hour
    schedules = db.get_schedules_by_hour(hour)
    for sch in schedules:
        word = db.get_word(sch.user_id)
        db.save_user_word(sch.user_id, word.id)

        translations = translate_api.translate(word)
        try:
            if translations:
                bot.send_message(sch.user_id, f"Here's a new word: \r\n{word.word} - {';'.join(translations)}")
            else:
                bot.send_message(sch.user_id, f"Here's a new word: \r\n{word.word} - {word.translation}")
        except ApiTelegramException as e:
            print(e)


def start_scheduler():
    scheduler.add_job(send_words_job, trigger="cron", minute=0)  # every hour
    scheduler.start()


def main():
    print('Бот стартовал')
    Thread(target=start_scheduler, args=()).start()
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.add_custom_filter(custom_filters.IsDigitFilter())
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
