import itertools
import functools
import collections

directions = {
    "forward": lambda value: (value, 0),
    "down": lambda value: (0, value),
    "up": lambda value: (0, -value) 
}

print(
    functools.reduce(
        lambda pos, dir: (pos[0] + dir[0], pos[1] + dir[1]),
        map(
            lambda command: directions[command[0]](int(command[1])), 
            map(
                lambda line: line.split(" "), 
                open("input.txt")
            )
        ),
        (0, 0)
    )
)