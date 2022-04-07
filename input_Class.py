import os
import pandas as pd


class InputData:
    """Класс, реализующий ввод от пользователя

        :param loans_file: Путь к файлу c займами
        :type loans_file: str

        :param mpi_file: Путь к файлу c MPI
        :type mpi_file: str

        output_data: dict
            Данные, полученные в результате ввода.
            Структура зависит от output_data['chart_type']

            Если output_data['chart_type'] == 'bar':
                Соответствует :return: к методу .bar_plot()

            Если output_data['chart_type'] == 'hist':
                Соответствует :return: к методу .hist_plot()

            Если output_data['chart_type'] == 'scatter':
                Соответствует :return: к методу .scatter_plot()

        """

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
            "1 - Столбчатая диаграмма\n"
            "2 - Гистограмма\n"
            "3 - Точечный график"
        )
        while True:

            reply = input('Какой график построить? ') \
                .replace(' ', '')

            # Проверяем корректность ответа
            if reply in ('1', '2', '3'):
                break

            else:
                print('Неверный ввод. Пожалуйста введите номер графика, '
                      'который нужно построить')

        if '1' == reply:
            return self.bar_plot()

        elif '2' == reply:
            return self.hist_plot()

        elif '3' == reply:
            return self.scatter_plot()

    def __input_file(self) -> str:
        print('\n1 - {}'.format(self.loans_path),
              '2 - {}'.format(self.mpi_path), sep='\n')

        while True:
            reply = input('Выберете файл с данными: ') \
                .replace(' ', '')

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
              '0 - не прозрачный\n'
              '100 - невидимый\n')

        while True:
            reply = input('Введите прозрачность: ') \
                .replace(' ', '')

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
    def __input_axis(types: dict, axis: str) -> str:
        while True:
            reply = input('Выберете столбец для оси {}: '.format(axis.upper()))

            if reply in types:
                return reply

            else:
                print('Такого столбца нет, введите столбец из списка выше')

    @staticmethod
    def __agg() -> int:
        while True:
            reply = int(input(
                'Выберете агрегирующую функцию \n'
                '1 - среднее, 2 - медиана, 3 - мода, \n'
                '4 - количество, 5 - количество уникальных значени\n'
                '0 - без агрегирования\n'
                'Номер агрегирующей функции: '))

            if reply in [1, 2, 3, 4, 5, 0]:
                return reply

            else:
                print('Такой функции нет')

    def bar_plot(self) -> dict:
        """Метод для ввода информации о столбчатой диаграмме

            :rtype: dict
            :return: {
                    :rtype chart_type: str
                    :return chart_type: тип графика = 'bar'

                    :rtype file: str
                    :return file: путь к файлу

                    :rtype dataframe: pd.DataFrame
                    :return dataframe: Dataframe с нужными данными

                    :rtype column_x: Any
                    :return column_x: название выбранной колонки для оси X

                    :rtype column_y: Any
                    :return column_y: название выбранной колонки для оси Y

                    :rtype alpha: float
                    :return alpha: прозрачность графика от 0 до 1
                }
        """

        output_data = {'chart_type': 'bar', 'file': self.__input_file()}
        df = pd.read_csv(output_data['file'])
        types = dict(df.dtypes)

        print('\nСтолбцы:')
        for t in types.keys():
            print('\t', t)

        for ax in ('x', 'y'):
            output_data[f'column_{ax}'] = self.__input_axis(types, ax)

        output_data['alpha'] = self.__input_alpha()
        output_data['agg'] = self.__agg()

        return output_data

    def hist_plot(self) -> dict:
        """Метод для ввода информации о гистограмме

            :rtype: dict
            :return: {
                    :rtype str:
                    :return chart_type: тип графика = 'hist'

                    :rtype str:
                    :return file: путь к файлу

                    :rtype pd.DataFrame:
                    :return dataframe: Dataframe с нужными данными

                    :rtype Any:
                    :return column_x: название выбранной колонки для оси X

                    :rtype Any:
                    :return column_y: название выбранной колонки для оси Y

                    :rtype float:
                    :return alpha: прозрачность графика от 0 до 1
                }
        """

        output_data = {'chart_type': 'hist', 'file': self.__input_file()}
        df = pd.read_csv(output_data['file'])
        types = dict(df.dtypes)

        print('\nСтолбцы:')
        for t in types.keys():
            print('\t', t)

        output_data[f'column_x'] = self.__input_axis(types, 'x')

        output_data['alpha'] = self.__input_alpha()
        return output_data

    def scatter_plot(self) -> dict:
        """Метод для ввода информации о точечном графике

            :rtype: dict
            :return: {
                    :rtype str:
                    :return chart_type: тип графика = 'scatter'

                    :rtype str:
                    :return file: путь к файлу

                    :rtype pd.DataFrame:
                    :return dataframe: Dataframe с нужными данными

                    :rtype Any:
                    :return column_x: название выбранной колонки для оси X

                    :rtype Any:
                    :return column_y: название выбранной колонки для оси Y

                    :rtype Any:
                    :return hue: название выбранной колонки для выделения оттенком

                    :rtype float:
                    :return alpha: прозрачность графика от 0 до 1
                }
        """

        output_data = {'chart_type': 'scatter', 'file': self.__input_file()}
        df = pd.read_csv(output_data['file'])
        types = dict(df.dtypes)

        print('\nСтолбцы:')
        for t in types.keys():
            print('\t', t)

        for ax in ('x', 'y'):
            output_data[f'column_{ax}'] = self.__input_axis(types, ax)

        output_data['alpha'] = self.__input_alpha()
        return output_data
