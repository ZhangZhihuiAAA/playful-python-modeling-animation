from random import uniform


N = 100000000
Nc = 0

for _ in range(N):
    x = uniform(0, 1.0)
    y = uniform(0, 1.0)
    if x ** 2 + y ** 2 < 1:
        Nc += 1

pi = 4 * Nc / N

print(f"Pi is {pi}")