import functools
import itertools
import copy


# input = list(map(lambda line: list(map(int, filter(lambda c: c != "\n", list(line)))), open("input.txt", "r")))

# positions = [(-1 -1j), (0 -1j), (1 -1j), (-1 +0j), (1 +0j), (-1 +1j), (0 +1j), (1 +1j)]

# def x(data):
#     to_flash = []
#     flashed = []
#     for i in range(0, 100):
#         data[int(i / 10)][i % 10] += 1
#         if data[int(i / 10)][i % 10] == 10:
#             to_flash.append(i)

#         while len(to_flash) > 0:
#             y = to_flash.pop()
#             flashed.append(y)
#             for position in filter(
#                 lambda pos: min(pos[0], pos[1]) >= 0 and max(pos[1], pos[0]) < 10, ((int(y / 10) + int(p.real), y % 10 + int(p.imag)) for p in positions)
#                 ):
#                 data[position[0]][position[1]] += 1

#                 if data[position[0]][position[1]] == 10:
#                     to_flash.append(position[0] * 10 + position[1])


#     for i in flashed:
#         data[int(i / 10)][i % 10] = 0
#     return data, len(flashed)

# count = 0


# data = copy.deepcopy(input)
# for step in range(0, 100):
#     data, flashes = x(data)
#     count += flashes
# print(count)

# data = copy.deepcopy(input)
# flashes = 0
# step = 0
# while flashes < 100:
#     step += 1 
#     data, flashes = x(data)
# print(step)

####

# pos = 1 + 3j
# test_positions = [ 0, 0 - 1j, 0 - 5j, -1, -1 + 1j, -5 + 4j, 1, 1 + 1j, 4j, 9j, 9, 10, 9 + 4j, 9 + 10j, 10 + 10j, 10 - 1j, 10 - 10j ]
# itertools.filterfalse(is_out_of_bounds, test_positions)

# list(functools.reduce(lambda acc, matrix: map(sum, zip(acc, matrix)), map(one, filter(lambda pos: pos.real >= bound_min.real and pos.imag >= bound_min.imag, map(functools.partial(sum, [ 3 + 4j ]), positions)))))
# list(functools.reduce(lambda acc, matrix: map(sum, zip(acc, matrix)), map(one, itertools.filterfalse(is_out_of_bounds, map(functools.partial(sum, [ 3 + 4j ]), flash_positions)))))


####

data = list(itertools.chain.from_iterable(map(lambda line: list(map(int, filter(lambda c: c != "\n", list(line)))), open("sample.txt", "r"))))
side = 10
size = side ** 2
bound_min = 0
bound_max = complex(side - 1, side - 1)

r = lambda x, repeat: itertools.repeat(x, int(repeat.imag * 10 + repeat.real))
one = lambda val, number: itertools.chain(r(0, number), [ val ], r(0, bound_max - number))

norm = lambda a, b: map(lambda x: x // abs(x), itertools.repeat(a - b, int(abs(a - b))))
check_dir = lambda a, b, dir: next(map(lambda n: dir - n, norm(a, b)), 0)
is_out_of_bounds = lambda pos: sum(map(lambda z: abs(check_dir(*z)), zip([ pos.real, pos.imag, pos.real, pos.imag ], [ bound_min.real, bound_min.imag, bound_max.real, bound_max.imag ], [1, 1, -1, -1])))
pos2complex = lambda pos: complex(pos % side, pos // side)

flash_positions = [(-1 -1j), (0 -1j), (1 -1j), (-1 +0j), (1 +0j), (-1 +1j), (0 +1j), (1 +1j)]

flash = lambda pos: \
    functools.reduce(
        lambda acc, matrix: map(sum, zip(acc, matrix)), 
        itertools.chain(
            map(
                functools.partial(one, -9),
                [ pos ]
            ),
            map(
                functools.partial(one, 1), 
                itertools.filterfalse(
                    is_out_of_bounds,
                    map(
                        functools.partial(sum, start=pos),
                        map(lambda i: [i], flash_positions)
                    )
                )
            )
        )
    )

sum_matrices = lambda ma, mb: list(map(sum, zip(ma, mb)))

apply_increase = lambda input: \
    itertools.accumulate(
        itertools.repeat([1] * size),
        sum_matrices,
        initial=input
    )

apply_flashes = lambda input: \
    functools.reduce(
        lambda acc, x: list(map(lambda za: max(min(za[0] + za[1], 10), 0) if za[1] >= 0 and za[0] > 0 else 0, zip(acc, x))),
        map(
            lambda z: flash(pos2complex(z[0])),
            itertools.filterfalse(
                lambda z: z[1],
                zip(
                    range(0, 10 * 10),
                    map(lambda x: x - 10, input)
                )
            )
        ),
        input
    )

repeat_apply_increase = lambda input: \
    itertools.dropwhile(
        lambda d: (10 not in d),
        apply_increase(input)
    )

repeat_apply_flashes = lambda input: \
    itertools.dropwhile(
        lambda d: (10 in d),
        itertools.accumulate(
            itertools.count(1),
            lambda acc, _: apply_flashes(acc),
            initial=input
        )
    )   

steps = lambda input: \
    itertools.accumulate(
        itertools.count(1),
        lambda acc, _: next(repeat_apply_flashes(next(repeat_apply_increase(acc)))),
        initial=input
    )


def print_map(step, side=10):
    step = list(step)
    for i in range(0, side):
        print(step[i*side:(i+1)*side])
    print()


# print_map(flash(3 + 4j))
for mapi, mapx in enumerate(itertools.islice(steps(data), None, 10)):
    print("After step", mapi + 1)
    print_map(mapx)