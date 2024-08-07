from random import uniform


N = 100000
DISTANCE = 10
DAY_LENGTH = 10 * 2 * DISTANCE  # 10 loops

towards = 0
for _ in range(N):
    s = uniform(0, DAY_LENGTH)
    src = uniform(0, DISTANCE)
    dst = uniform(0, DISTANCE)
    bus_loc = s % (2 * DISTANCE)

    bus_sbs = src <= bus_loc <= 2 * DISTANCE - src
    bus_sas = bus_loc <= src or bus_loc >= 2 * DISTANCE - src

    if src >= dst and bus_sbs or src < dst and bus_sas:
        towards += 1

print(towards / N)