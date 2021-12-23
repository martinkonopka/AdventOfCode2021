import functools
import itertools
import copy


input = list(map(lambda line: list(map(int, filter(lambda c: c != "\n", list(line)))), open("input.txt", "r")))

positions = [(-1 -1j), (0 -1j), (1 -1j), (-1 +0j), (1 +0j), (-1 +1j), (0 +1j), (1 +1j)]

def x(data):
    to_flash = []
    flashed = []
    flashes = 0
    for i in range(0, 100):
        data[int(i / 10)][i % 10] += 1
        if data[int(i / 10)][i % 10] == 10:
            to_flash.append(i)

        while len(to_flash) > 0:
            y = to_flash.pop()
            flashed.append(y)
            # print(y, "----")
            for position in filter(lambda pos: min(pos[0], pos[1]) >= 0 and max(pos[1], pos[0]) < 10, ((int(y / 10) + int(p.real), y % 10 + int(p.imag)) for p in positions)):
                # print(position)
                data[position[0]][position[1]] += 1

                if data[position[0]][position[1]] == 10:
                    to_flash.append(position[0] * 10 + position[1])


    for i in flashed:
        data[int(i / 10)][i % 10] = 0
    return data, len(flashed)

count = 0


data = copy.deepcopy(input)
for step in range(0, 100):
    # print("-----")
    # for line in  range(0, len(input)):
    #     print(input[line])
    data, flashes = x(data)
    count += flashes
print(count)

data = copy.deepcopy(input)
step = 0
while True:
    step += 1 
    data, flashes = x(data)
    if flashes == 100:
        print(step)
        break

    