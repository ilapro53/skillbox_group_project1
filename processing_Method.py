from typing import Any
from numpy import percentile


def clearing(series_for_cleaning: Any) -> Any:
    # функция удаляет строки с нулевыми значениями c сохранением в датафрейм
    return series_for_cleaning.dropna()


def outlier(series_q: Any, column: Any) -> Any:
    # функция для отсеивания выбросов (правило 3-х Сигм)
    series_q = series_q.reset_index()
    q75, q25 = percentile(series_q[column], [75, 25])
    interval_qr = q75 - q25
    max_df = q75 + (1.5 * interval_qr)
    min_df = q25 - (1.5 * interval_qr)
    data_99_perc = series_q[(series_q[column] >= min_df)
                            & (series_q[column] <= max_df)]
    return data_99_perc


def processing_bar(data: Any, col_for_agg: str, colon: str, agg: int) -> Any:
    # функция обрабатывает/преобразовывает данные для создания столбчатой диаграммы
    # agg - хранит число от 1 до 4, где
    # 1 - среднее, 2 - медиана, 3 - сумма, 4 - кол-во уникальных значений
    # col_for_agg - название колонки для агрегации
    # colon - колонка с категориями
    df = data[[col_for_agg, colon]]
    df = clearing(df)
    if agg == 1:
        df = df.groupby(col_for_agg).mean()[[colon]]
    elif agg == 2:
        df = df.groupby(col_for_agg).median()[[colon]]
    elif agg == 3:
        df = df.groupby(col_for_agg).count()[[colon]]
    elif agg == 4:
        df = df.groupby(col_for_agg).nunique()[[colon]]
    return df


def processing_hist(data: Any, column: str) -> Any:
    # функция обрабатывает/преобразовывает данные для создания гистограммы
    series_data = data[column]
    series_data = clearing(series_data).reset_index()
    series_data = outlier(series_data, column)
    return series_data[column]


def processing_scatter(data: Any, column_1: str, column_2: str) -> Any:
    # функция обрабатывает/преобразовывает данные для создания точечной диаграммы
    df = data[[column_1, column_2]]
    df = clearing(df)
    df = outlier(df, column_1)
    df = outlier(df, column_2)
    return df
