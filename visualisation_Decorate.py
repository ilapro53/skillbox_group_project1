from typing import Any

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from jupyterthemes import jtplot

from processing_Method import processing_bar, processing_hist, processing_scatter

jtplot.style(theme='oceans16', context='notebook', ticks=True, grid=False)


class PreparationVisualisedData:
    class Wrapped:

        """Класс-декоратор, выполняющий подготовку и объединение данных
        перед прорисовкой графиков на основе данных
        файла input_Class.py, а затем и
        файла processing_Method.py"""

        def __init__(self, data: dict, func: Any) -> None:
            # print(func, data)

            self.func: Any = func
            self.input_data: dict = data
            self.fig, self.ax = plt.subplots(figsize=(20, 11))
            if self.input_data['chart_type'] != 'bar':
                self.ax.set_xlabel(self.input_data['column_x'], fontsize=16)
                if self.input_data['chart_type'] == 'scatter':
                    self.ax.set_ylabel(self.input_data['column_y'], fontsize=16)
            self.output_file_name_object = 'graph'
            self()

        def __call__(self) -> None:
            if self.input_data['chart_type'] == 'bar':
                self.preparation_bar()
            elif self.input_data['chart_type'] == 'hist':
                self.preparation_hist()
            elif self.input_data['chart_type'] == 'scatter':
                self.preparation_scatter()

            self.func(self.output_file_name_object, self.fig)

        def preparation_bar(self) -> None:
            processing_data = processing_bar(pd.read_csv(self.input_data['file']),
                                             self.input_data['agg'])
            self.ax.bar(list(processing_data.index), processing_data,
                                   alpha=self.input_data['alpha'])
            self.ax.tick_params(axis='x', rotation=30)

        def preparation_hist(self) -> None:
            processing_data = processing_hist(pd.read_csv(self.input_data['file']),
                                              self.input_data['column_x'])
            self.ax.hist(processing_data, alpha=self.input_data['alpha'])

        def preparation_scatter(self) -> None:
            processing_data = processing_scatter(pd.read_csv(self.input_data['file']),
                                                 self.input_data['column_x'],
                                                 self.input_data['column_y'])
            self.ax.scatter(processing_data[self.input_data['column_x']],
                                       processing_data[self.input_data['column_y']],
                                       alpha=self.input_data['alpha'])

    def __init__(self, func):
        self.func = func

    def __call__(self, data: dict):
        return PreparationVisualisedData.Wrapped(func=self.func, data=data)


@PreparationVisualisedData
# Отрисовка и сохранение графика в формате .png
def save_and_visualised_data(output_file_name_object, fig) -> Any:
    # plt.show()
    fig.savefig(f'{output_file_name_object}.png', format='png')
