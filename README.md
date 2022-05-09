# Групповой проект Skillbox

### Задачи распределяются следующим образом:
#### 1 человек делает первый класс:
В нем сделан ввод от пользователя данных и параметров, и создание объекта с атрибутами, к атрибутам которого можно обратиться из второго класса.
Надо реализовать ввод следующих данных:
  1. Номер нужной функции из списка
  2. Какой тип графика нужен
  3. Название файла, куда будет сохранена фотография графика <br />

Это всё сохраняется в атрибуты, которые идут дальше.
#### 2 человека делают второй класс:
В нем он принимает объект с атрибутами первого класса, и на основе этих данных вызывает вызывает определенные функции с сегрегацией данных (группировка с агрегирующей функцией, очистка пустых значений и то, что сможете придумать).

Выходом должен быть готовый датафрейм, который нужен для построения графика.
#### 1 человек делает третий класс:
В нем функции, рисующие графики на основе данных, полученных из готового датафрейма из второй группы, и сохранение их в файл.
Принимает датафрейм, и итогом должно быть сохранение в файл.
