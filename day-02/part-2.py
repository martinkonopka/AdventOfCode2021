import itertools
import functools
import collections

directions = {
    "forward": lambda pos, value: (pos[0] + value, pos[1] + pos[2] * value, pos[2]),
    "down": lambda pos, value: (pos[0], pos[1], pos[2] + value),
    "up": lambda pos, value: (pos[0], pos[1], pos[2] - value) 
}

final = functools.reduce(
    lambda pos, dir: dir[0](pos, dir[1]),
    map(
        lambda command: (directions[command[0]], int(command[1])), 
        map(
            lambda line: line.split(" "), 
            open("input.txt")
        )
    ),
    (0, 0, 0)
)

print(final[0] * final[1])