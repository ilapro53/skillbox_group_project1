from typing import Any
from matplotlib import pyplot as plt
import pandas as pd
from jupyterthemes import jtplot

import input_Class
import processing_Method

jtplot.style(theme='oceans16', context='notebook', ticks=True, grid=False)
#test

class PreparationVisualisedData:
    """Класс-декоратор, выполняющий подготовку и объединение данных
    перед прорисовкой графиков на основе данных
    файла input_Class.py, а затем и
    файла processing_Method.py"""

    def __init__(self, func: Any) -> None:
        self.func: Any = func
        loans = 'kiva_loans.csv'
        mpi = 'kiva_mpi_region_locations.csv'
        self.input_data: dict = input_Class.InputData(loans, mpi)()
        self.fig, self.ax = plt.subplots(figsize=(15, 8))
        self.ax.set_xlabel(self.input_data['column_x'], fontsize=16)
        if self.input_data['chart_type'] != 'hist':
            self.ax.set_ylabel(self.input_data['column_y'], fontsize=16)
        self.output_file_name_object = 'graph'

    def __call__(self) -> None:
        if self.input_data['chart_type'] == 'bar':
            self.preparation_bar()
        elif self.input_data['chart_type'] == 'hist':
            self.preparation_hist()
        elif self.input_data['chart_type'] == 'scatter':
            self.preparation_scatter()

        self.func(self.output_file_name_object, self.fig)

    def preparation_bar(self) -> None:
        processed_data = processing_Method.bar(pd.read_csv(self.input_data['file']),
                                               self.input_data['column_x'],
                                               self.input_data['column_y'],
                                               self.input_data['agg'])
        self.ax.bar(processed_data[self.input_data['column_x']],
                    processed_data[self.input_data['column_y']],
                    alpha=self.input_data['alpha'])

    def preparation_hist(self) -> None:
        processed_data = processing_Method.hist(pd.read_csv(self.input_data['file']),
                                                self.input_data['column_x'])
        self.ax.hist(processed_data, alpha=self.input_data['alpha'])

    def preparation_scatter(self) -> None:
        processed_data = processing_Method.scatter(pd.read_csv(self.input_data['file']),
                                                   self.input_data['column_x'],
                                                   self.input_data['column_y'])
        self.ax.scatter(processed_data[self.input_data['column_x']],
                        processed_data[self.input_data['column_y']],
                        alpha=self.input_data['alpha'])


@PreparationVisualisedData
# Отрисовка и сохранение графика в формате .png
def Save_and_Visualised_Data(output_file_name_object, fig) -> Any:
    plt.show()
    fig.savefig(f'{output_file_name_object}.png', format='png')


Save_and_Visualised_Data()
