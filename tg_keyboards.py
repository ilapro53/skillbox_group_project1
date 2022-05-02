from telebot import types
from main import InputData


def home_keyboard():
    keyb = types.ReplyKeyboardMarkup(one_time_keyboard=False,
                                     resize_keyboard=True)

    keyb.add(types.KeyboardButton('Новый график'))

    return keyb


def choose_file_keyboard(cls: InputData):
    keyb = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                     resize_keyboard=True)
    for name in (cls.mpi_path, cls.loans_path):
        keyb.add(types.KeyboardButton(name))

    return keyb


def choose(titles: iter, rw: int or None = None):
    if rw is None:
        if len(titles) <= 3:
            rw = 1
        else:
            rw = 2

    keyb = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                     resize_keyboard=True,
                                     row_width=rw)
    keyb.add(*titles)
    return keyb
