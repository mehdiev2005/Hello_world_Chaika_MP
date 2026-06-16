n = int(input('Введите число: '))
fact = 1
i = 1

while i<=n:
    fact *= i
    i += 1

print(fact)