s = input()

cnt = [0] * 26

for c in s:
    cnt[ord(c) - ord('A')] += 1

n = len(s)

for x in cnt:
    if x > n // 2:
        print(-1)
        exit()

arr = []

for i in range(26):
    arr += [chr(i + 65)] * cnt[i]

m = n // 2

a = arr[:m]
b = arr[m:]

b = b[1:] + b[:1]

for i in range(m):
    if a[i] == b[i]:
        print(-1)
        exit()

print(''.join(a))
print(''.join(b))