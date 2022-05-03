from telebot import TeleBot
from typing import Any

bot = TeleBot('5389116596:AAFw_f7dqwbEW6YDMVNzTuZhSw3e5JmwcU8')
# Бот: @skillbox_project_testbot

import tg_keyboards
from input_Class import InputData

# Каждый аккаунт Telegram имеет свой класс InputData,
# чтобы разные пользователи могли пользоваться ботом
# одновременно
sessions: dict[Any: InputData] = {}


@bot.message_handler(content_types=['text', 'document', 'audio'])
def simple_massage_handler(message):
    if message.from_user.id not in sessions:
        sessions[message.from_user.id] = InputData(
            loans_file='kiva_loans.csv',
            mpi_file='kiva_mpi_region_locations.csv')
    user_input = sessions[message.from_user.id]
    if message.text == '/start':
        sessions[message.from_user.id] = InputData(
            loans_file='kiva_loans.csv',
            mpi_file='kiva_mpi_region_locations.csv')
        bot.send_message(message.from_user.id,
                         f'Здравствуйте. Нажмите "Новый график" '
                         f'чтобы начать строить график',
                         reply_markup=tg_keyboards.home_keyboard())
    elif user_input.bot_path == []:
        user_input.page_home(message)
    elif user_input.bot_path == ['new_plot']:
        user_input.page_new_plot(message)
    elif user_input.bot_path == ['new_plot', 'plot']:
        user_input.page_input_file(message)
    elif user_input.bot_path == ['new_plot', 'plot', 'file']:
        user_input.page_input_axis(message)
    elif user_input.bot_path == ['new_plot', 'plot', 'file', 'axis']:
        user_input.page_input_alpha(message)
    elif user_input.bot_path == ['new_plot', 'plot', 'file', 'axis', 'agg']:
        user_input.page_input_agg(message)
    else:
        raise ValueError(f'Неожиданный путь {user_input.bot_path}')


def start_bot():
    print('Запуск бота...')
    while True:
        bot.polling()


if __name__ == '__main__':
    start_bot()
