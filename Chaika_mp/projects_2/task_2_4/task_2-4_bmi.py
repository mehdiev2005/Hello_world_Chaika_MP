weight = float(input('Введите ваш вес, кг: '))
height = float(input('Введите ваш рост, м: '))


print('--- Отчёт о состоянии здоровья --- ',
      f'Рост:\t {height} см',
      f'Вес:\t {weight} кг',
      f'ИМТ:\t {weight / (height ** 2)}',
      sep='\n')
