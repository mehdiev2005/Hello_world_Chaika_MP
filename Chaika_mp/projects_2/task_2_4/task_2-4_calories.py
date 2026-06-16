proteins = float(input('Введите количество белков, г: '))
fats = float(input('Введите количество жиров, г: '))
carbs = float(input('Введите количество углеводов, г: '))


print(f'Калорийность продукта - {proteins*4+fats*9+carbs*4} ккал.')
