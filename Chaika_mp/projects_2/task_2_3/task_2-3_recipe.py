name = input('Название питательной среды: ')
agar_percentage = float(input('Введите концентрацию агара, %: '))
sterilization_temp = float(input('Введите температуру стерилизации, °C: '))


with open("C:/Users/Михаил Чайка/Documents/Python/Chaika_mp/projects_2/task_2_3/recipe.txt", "w", encoding="utf-8") as recipe:
    recipe.write(f'Название среды: {name} \n ================================================== \n Концентрация агара = {agar_percentage} \n Температура стеризилации = {sterilization_temp} °C')

print('Файл \'recipe.txt\' успешно сформирован!')
