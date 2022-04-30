import os
import pandas as pd


class InputData:
    """Класс, реализующий ввод от пользователя"""

    def __init__(self, loans_file: str, mpi_file: str) -> None:
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

    def __call__(self) -> dict:
        # Спрашиваем тип графика
        print(
            "\t1 - Столбчатая диаграмма\n"
            "\t2 - Гистограмма\n"
            "\t3 - Точечный график"
        )
        while True:
            reply = input('Какой график построить? ').replace(' ', '')
            # Проверяем корректность ответа
            if reply in ('1', '2', '3'):
                break
            else:
                print('Неверный ввод. Пожалуйста введите номер графика, '
                      'который нужно построить')
        if '1' == reply:
            return self.__plot('bar')
        elif '2' == reply:
            return self.__plot('hist')
        elif '3' == reply:
            return self.__plot('scatter')

    def __input_file(self) -> str:
        print('\nФайлы с данными:\n'
              '\t1 - {}'.format(self.loans_path),
              '\t2 - {}'.format(self.mpi_path), sep='\n')
        while True:
            reply = input('Выберете файл: ').replace(' ', '')
            if reply == '1':
                return self.loans_path
            elif reply == '2':
                return self.mpi_path
            else:
                print('Неверный ввод. Пожалуйста введите номер файла, '
                      'из которого нужно взять данные')

    @staticmethod
    def __input_alpha() -> float:
        print('\nПрозрачность графика в процентах\n'
              '\t0 - не прозрачный\n'
              '\t100 - невидимый')
        while True:
            reply = input('Введите прозрачность: ').replace(' ', '')
            try:
                reply = float(reply) / 100
                if reply > 1 or reply < 0:
                    print('Неверное значение. Прозрачность не '
                          'может быть больше 100 или меньше 0.')
                else:
                    return reply
            except ValueError:
                print('Неверный ввод. Пожалуйста введите номер файла, '
                      'из которого нужно взять данные')

    @staticmethod
    def __input_axis(cols_dict: dict, axis: str) -> str:
        while True:
            reply = input('Выберете столбец для оси {}: '.format(axis.upper()))
            if reply in cols_dict:
                return reply
            else:
                print('Такого столбца нет, введите столбец из списка выше')

    @staticmethod
    def __agg() -> int:
        while True:
            reply = int(input(
                '\nВыберете агрегирующую функцию\n'
                '\t1 - среднее, 2 - медиана,\n'
                '\t3 - дисперсия, 4 - кол-во уникальных значений\n'
                'Номер агрегирующей функции: '))
            if reply in [1, 2, 3, 4]:
                return reply
            else:
                print('Такой функции нет')

    def __plot(self, chart_type: str) -> dict:
        """Метод для ввода информации для соответствующего графика"""
        output_data = {'chart_type': chart_type, 'file': self.__input_file()}

        df = pd.read_csv(output_data['file'])
        cols_dict = dict(df.dtypes)

        # Вывод подходящих имен столбцов
        print('\nСтолбцы:')
        for name in cols_dict:
            if chart_type != 'bar':
                if (cols_dict[name] == 'float64') or (cols_dict[name] == 'int64'):
                    print('\t', name)
            elif len(df[name].unique()) < 120:
                print('\t', name)

        # Ввод с проверкой существования столбцов
        if output_data['chart_type'] == 'scatter':
            for ax in ('x', 'y'):
                output_data[f'column_{ax}'] = self.__input_axis(cols_dict, ax)
        elif output_data['chart_type'] == 'hist':
            output_data[f'column_x'] = self.__input_axis(cols_dict, 'x')

        # Добавление агрегирующей функции (если bar)
        if output_data['chart_type'] == 'bar':
            output_data['agg'] = self.__agg()

        # Добавление прозрачности графика
        output_data['alpha'] = self.__input_alpha()

        return output_data
