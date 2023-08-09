import random

seen = {}
for _ in range(100000):
    i = random.randrange(6) - random.randrange(6)
    seen[i] = seen.get(i, 0) + 1
print(seen)
