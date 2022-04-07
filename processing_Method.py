import pandas as pd
import numpy as np


def find_column(data, column):
    # функция, которая проверяет существует ли искомый столбец в заданном датафрейме
    if column in data.columns:
        return True
    else:
        return False


def check_data(series_for_checking):
    # функция устанавливает/преобразовывает тип данных существующего столбца данных в тип float
    try:
        series_for_checking = series_for_checking.astype(float)
    except:
        print('Предполагается колонка с числовыми значениями')
        return False
    return True


def dropna(series_for_cleaning):
    # функция удаляет строки с нулевыми значениями
    return series_for_cleaning.dropna()


def outlier(series_q, column):
    # функция для отсеивания выбросов (правило 3х Сигм)
    series_q = series_q.reset_index()
    q75, q25 = np.percentile(series_q[column], [75, 25])
    interval_qr = q75 - q25
    max_df = q75 + (1.5 * interval_qr)
    min_df = q25 - (1.5 * interval_qr)
    data_99_perc = series_q[(series_q[column] >= min_df)
                            & (series_q[column] <= max_df)]
    return data_99_perc


def bar(data, col_of_categorias, col_for_agg, agg):
    # функция обрабатывает/преобразовывает данные для создания столбчатой диаграммы
    # agg - хранит число от 1 до 5, где
    # 1 - среднее, 2 - медиана, 3 - мода, 4 - количество, 5 - количество уникальных значений
    # col_for_agg - название колонки для агрегации
    # col_of_categorias - колонка с категориями
    if find_column(data, col_for_agg) == False:
        return print('Колонка {} не существует'.format(col_for_agg))
    if find_column(data, col_of_categorias) == False:
        return print('Колонка {} не существует'.format(col_of_categorias))
    try:
        if int(agg) in list(range(0, 6)):
            df = data[[col_of_categorias, col_for_agg]]
        else:
            return print('Неверный запрос для агрегация')
    except:
        return print('Неверный запрос для агрегация')
    if agg < 4:
        if check_data(df[col_for_agg]) == False:
            return
    df = dropna(df)
    if agg == 1:
        df = df.groupby(col_of_categorias)[col_for_agg].mean()
    elif agg == 2:
        df = df.groupby(col_of_categorias)[col_for_agg].median()
    elif agg == 3:
        df = df.groupby(col_of_categorias)[col_for_agg].agg(pd.Series.mode)
    elif agg == 4:
        df = df.groupby(col_of_categorias)[col_for_agg].count()
    elif agg == 5:
        df = df.groupby(col_of_categorias)[col_for_agg].nunique()
    elif agg == 0:
        pass
    return df


def hist(data, column):
    # функция обрабатывает/преобразовывает данные для создания гистограммы
    # data - датафрейм
    # column - название колонки, запрос в первом классе
    if find_column(data, column) == False:
        return print('Колонка {} не существует'.format(column))
    serie = data[column]
    if check_data(serie) == False:
        return print('Неверный формат данных')
    serie = dropna(serie).reset_index()
    serie = outlier(serie, column)
    return serie[column]


def scatter(data, column_1, column_2):
    # функция обрабатывает/преобразовывает данные для создания точечной диаграммы
    # column_outl - колонка для отсеивания выбросов
    if find_column(data, column_1) == False:
        return print('Колонка {} не существует'.format(column_1))
    if find_column(data, column_2) == False:
        return print('Колонка {} не существует'.format(column_2))
    df = data[[column_1, column_2]]
    if check_data(df[column_1]) == False or check_data(df[column_2]) == False:
        return
    df = dropna(df)
    return df
