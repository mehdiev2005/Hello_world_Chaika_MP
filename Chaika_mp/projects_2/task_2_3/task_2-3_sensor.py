name = input('Введите имя оператора: ')
pressure = input('Введите текущее значение давления: ')


with open("C:/Users/Михаил Чайка/Documents/Python/Chaika_mp/projects_2/task_2_3/sensor_log.txt", "w", encoding="utf-8") as recipe:
    recipe.write(f'{name}\t{pressure}')

print('Данные успешно сохранены в файл sensor_log.txt')
