a = [2, 3, -55, 545641, 0, -144, 2.555]
l = len(a)
counter = 0

for i in range (0, l):
    if a[i]>0:
        counter += 1

print(counter)
