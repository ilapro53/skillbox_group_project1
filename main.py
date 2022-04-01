import input
import processing
import visualisation

loans = 'kiva_loans.csv'
mpi = 'kiva_mpi_region_locations.csv'
# Просьба добавить датасеты в .gitignore

input_data = input.InputData(loans, mpi)
# Ввод данных от пользователя и сохранение в переменную

processed_data = processing.ProcessedData(input_data)
# Обработка и сохранение этих данных в переменную

output_file_name = 'graph.png'
visualisation.VisualisedData(processed_data, output_file_name)
# Отрисовка графиков, и сохранение их в файл
