import os
from typing import List, Iterable, Dict

import pandas as pd

import tg_keyboards
from main import bot
from visualisation_Decorate import save_and_visualised_data


class InputData:
    agg_list: dict[str, str] = {
        'среднее': 'mean',
        'медиана': 'median',
        'дисперсия': 'var',
        'количество уникальных значений': 'nunique'
    }

    def __init__(self, loans_file: str, mpi_file: str) -> None:
        self.bot_path = []
        self.data = {'axis': {}}
        self.axis_list = None

        # Проверяем наличие файла loans
        if os.path.exists(loans_file):
            self.loans_path = loans_file
        else:
            raise FileExistsError('Файла {} не найдено'.format(loans_file))

        # Проверяем наличие файла mpi
        if os.path.exists(mpi_file):
            self.mpi_path = mpi_file
        else:
            raise FileExistsError('Файла {} не найдено'.format(mpi_file))

    def _clos_list(self):
        cols_dict = dict(self.data['dataframe'])

        # cols = cols_dict
        cols = []
        for name in cols_dict:
            if self.data['chart_type'] != 'bar':
                if cols_dict[name].dtype in ['float64', 'int64']:
                    cols.append(name)
            elif len(self.data['dataframe'][name].unique()) < 120:
                cols.append(name)

        return cols

    def build(self, msg):

        for name, value in self.data['axis'].items():
            self.data[f'column_{name}'] = value

        del (self.data['axis'])

        save_and_visualised_data(self.data)

        with open('graph.png', 'rb') as photo:
            bot.send_photo(msg.from_user.id,
                           photo,
                           caption='Ваш график',
                           reply_markup=tg_keyboards.home_keyboard())

        self.bot_path = []

    def page_home(self, msg):
        if msg.text == 'Новый график':
            self.bot_path = ['new_plot']
            bot.send_message(msg.from_user.id,
                             f'Хорошо, новый график. '
                             f'Выберите тип графика',
                             reply_markup=tg_keyboards.choose(
                                     (
                                         'Столбчатая диаграмма',
                                         'Гистограмма',
                                         'Точечный график'
                                     )
                                 )
                             )

        else:
            bot.send_message(msg.from_user.id,
                             'Неверная команда. Нажмите "Новый график", '
                             'чтобы начать строить график',
                             reply_markup=tg_keyboards.home_keyboard())

    def page_new_plot(self, msg):
        if msg.text == 'Столбчатая диаграмма':
            self.bot_path = ['new_plot', 'plot']
            self.data['chart_type'] = 'bar'
            bot.send_message(msg.from_user.id,
                             f'Итак, строим столбчатую диаграмму. Выберите '
                             f'файл с данными',
                             reply_markup=tg_keyboards.choose_file_keyboard(self))

        elif msg.text == 'Гистограмма':
            self.bot_path = ['new_plot', 'plot']
            self.data['chart_type'] = 'hist'
            bot.send_message(msg.from_user.id,
                             f'Итак, строим гистограмму. Выберите '
                             f'файл с данными',
                             reply_markup=tg_keyboards.choose_file_keyboard(self))

        elif msg.text == 'Точечный график':
            self.bot_path = ['new_plot', 'plot']
            self.data['chart_type'] = 'scatter'
            bot.send_message(msg.from_user.id,
                             f'Итак, строим точечный график. Выберите '
                             f'файл с данными',
                             reply_markup=tg_keyboards.choose_file_keyboard(self))

        else:
            bot.send_message(msg.from_user.id,
                             'Неверная команда. Выберите один из предложенных '
                             'графиков',
                             reply_markup=tg_keyboards.choose(
                                     (
                                         'Столбчатая диаграмма',
                                         'Гистограмма',
                                         'Точечный график'
                                     )
                                 )
                             )

    def page_input_file(self, msg):
        if msg.text in (self.mpi_path,
                        self.loans_path):

            self.bot_path.append('file')
            self.data['file'] = msg.text
            bot.send_message(msg.from_user.id,
                             f'Загрузка данных из файла "{msg.text}" ...')

            if 'file' not in self.data or \
                    'dataframe' not in self.data:
                self.data['file'] = msg.text
                self.data['dataframe'] = pd.read_csv(msg.text)


            if self.data['chart_type'] in ('bar', 'scatter'):
                self.axis_list = ['x', 'y']
            else:
                self.axis_list = ['x']

            cols = self._clos_list()

            bot.send_message(msg.from_user.id,
                             f'Выберите колонку X из файла',
                             reply_markup=tg_keyboards.choose(cols))

        else:
            bot.send_message(msg.from_user.id,
                             'Неверная команда. Выберите файл с данными',
                             reply_markup=tg_keyboards.choose_file_keyboard(self))

    def page_input_axis(self, msg):

        cols = self._clos_list()

        if msg.text in cols:
            ax_name = self.axis_list[
                len(self.data['axis'])
            ]

            self.data['axis'].update({ax_name: msg.text})

            if len(self.data['axis']) != len(self.axis_list):
                ax_name = self.axis_list[
                    len(self.data['axis'])
                ]
                bot.send_message(msg.from_user.id,
                                 f'Выберите колонку {ax_name.upper()} из файла',
                                 reply_markup=tg_keyboards.choose(cols))

            else:
                self.bot_path.append('axis')
                bot.send_message(msg.from_user.id,
                                 f'Введите прозрачность графика в процентах (от 0 до 100)\n'
                                 '0 - не прозрачный\n'
                                 '100 - невидимый\n')

        else:
            ax_name = self.axis_list[
                len(self.data['axis'])
            ]
            bot.send_message(msg.from_user.id,
                             f'Неверная команда. Выберите столбец данных для оси {ax_name}',
                             reply_markup=tg_keyboards.choose(cols))

    def page_input_alpha(self, msg):
        try:
            answ = float(msg.text) / 100

            if answ > 1 or answ < 0:
                bot.send_message(msg.from_user.id,
                                 'Неверное значение. Прозрачность не '
                                 'может быть больше 100 или меньше 0')
            else:
                self.data['alpha'] = answ

                if self.data['chart_type'] == 'bar':
                    self.bot_path.append('agg')
                    bot.send_message(msg.from_user.id,
                                     f'Выберете агрегирующую функцию',
                                     reply_markup=tg_keyboards.choose(InputData.agg_list.keys()))

                else:
                    self.bot_path.extend(['agg', 'build'])
                    self.build(msg)

        except ValueError:
            bot.send_message(msg.from_user.id,
                             f'Неверное значение. Введите прозрачность числом')

    def page_input_agg(self, msg):

        if msg.text in InputData.agg_list:
            self.data['agg'] = InputData.agg_list[msg.text]

            self.bot_path.append('build')
            bot.send_message(msg.from_user.id,
                             f'Секунду. Строим график...')

            self.build(msg)

        else:
            bot.send_message(msg.from_user.id,
                             f'Неверное значение. Выберите агрегирующую функцию')
