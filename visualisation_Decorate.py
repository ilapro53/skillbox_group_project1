from typing import Any
from matplotlib import pyplot as plt
import pandas as pd
from jupyterthemes import jtplot

import input_Class
import processing_Method

jtplot.style(theme='oceans16', context='notebook', ticks=True, grid=False)


class PreparationVisualisedData:
    """Класс-декоратор, выполняющий подготовку и объединение данных
    перед прорисовкой графиков на основе данных
    файла input_Class.py, а затем и
    файла processing_Method.py"""

    def __init__(self, func: Any) -> None:
        self.func: Any = func
        self.input_data: dict = input_Class.result_InputData
        self.fig, self.ax = plt.subplots(figsize=(15, 8))
        self.alpha_in = self.input_data['alpha']
        self.ax.set_xlabel(self.input_data['column_x'], fontsize=16)
        self.ax.set_ylabel(self.input_data['column_y'], fontsize=16)

    def __call__(self, output_file_name_object: str) -> None:
        if self.input_data['chart_type'] == 'bar':
            processed_data = processing_Method.bar(pd.read_csv(self.input_data['file']),
                                                   self.input_data['column_x'],
                                                   self.input_data['column_y'],
                                                   self.input_data['agg'])
            self.ax.bar(processed_data[self.input_data['column_x']],
                        processed_data[self.input_data['column_y']])
        elif self.input_data['chart_type'] == 'hist':
            processed_data = processing_Method.hist(pd.read_csv(self.input_data['file']),
                                                    self.input_data['column_x'])
            self.ax.hist(processed_data)
        elif self.input_data['chart_type'] == 'scatter':
            processed_data = processing_Method.scatter(pd.read_csv(self.input_data['file']),
                                                       self.input_data['column_x'],
                                                       self.input_data['column_y'])
            self.ax.scatter(processed_data[self.input_data['column_x']],
                            processed_data[self.input_data['column_y']])

        self.func(output_file_name_object, self.fig, self.alpha_in)


@PreparationVisualisedData
# Отрисовка и сохранение графика в формате .png
def Save_and_Visualised_Data(output_file_name_object, fig, alpha_in) -> Any:
    plt.show(alpha=alpha_in)
    fig.savefig(output_file_name_object)


Save_and_Visualised_Data('graph.png')
