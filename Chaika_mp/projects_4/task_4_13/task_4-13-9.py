a = [2, 3, -55, 545641, 0, -144]
l = len(a)
res = 0

for i in range (0, l):
    if a[i]%2!=0:
        res += 1

print(res)