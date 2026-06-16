w = input('Введите число: ')
x = input('Введите число: ')
y = input('Введите число: ')
z = input('Введите число: ')

if w<x:
    min = w
else:
    min = x
if y<min:
    min = y
if z<min:
    min = z

print(min)