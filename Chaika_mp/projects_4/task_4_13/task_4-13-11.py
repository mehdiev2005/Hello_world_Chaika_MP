a = [2, 3, 55, 545641, 0, -144]
l = len(a)
res = 0
j = 0

for i in range (0, l-1):
    if i%2 == 0:
        j += 1
        res += a[i]
res = res/j
print(res)