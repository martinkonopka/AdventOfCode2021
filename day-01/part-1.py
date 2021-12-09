import itertools
import functools
import collections


# from: https://docs.python.org/3/library/itertools.html#itertools-recipes
def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) -> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(itertools.islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)

is_greater = lambda window: window[0] < window[1]

in1, in2 = itertools.tee(
    map(lambda value: int(value), open("input.txt"))
)


print(
    sum(
        map(is_greater, sliding_window(in1, 2))
    )
)

print(
    sum(
        map(
            is_greater, 
            sliding_window(
                map(
                    sum,
                    sliding_window(in2, 3)
                ),
                2
            )
        )
    )
)
