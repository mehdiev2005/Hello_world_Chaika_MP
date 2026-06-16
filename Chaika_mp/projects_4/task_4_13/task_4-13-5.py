n = int(input('Введите количество чисел: '))
a = float(input('Введите число: '))
i = 1

a = float(input('Введите число: '))
max = a
for i in range (1, n-1):
    b = float(input('Введите число: '))
    if b > max:
        max = b
    i += 1
print(max)