a = [2, 3, 55, 545641, 0, -144, 2.555]
l = len(a)
i = 0
res = 0

for i in range (0, l-1):
    res += a[i]

res = res/l
print(res)
