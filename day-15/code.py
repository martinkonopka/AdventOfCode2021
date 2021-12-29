import itertools
import functools
from collections import Counter

plan = functools.reduce(
    lambda acc, node: acc | node,
    itertools.chain.from_iterable(
        map(
            lambda zl: map(
                lambda zc: { complex(zc[0], zl[0]): int(zc[1]) },
                zip(itertools.count(), zl[1].strip())
            ),
            zip(itertools.count(), open("input.txt"))
        )
    ),
    {}
)

directions = [ (0 -1j), (-1 +0j), (1 +0j), (0 +1j) ]

norm = lambda a, b: map(lambda x: x // abs(x), itertools.repeat(a - b, int(abs(a - b))))
check_dir = lambda a, b, dir: next(map(lambda n: dir - n, norm(a, b)), 0)
get_is_out_of_bounds = lambda bounds: \
    lambda pos: sum(
        map(
            lambda z: abs(check_dir(*z)), 
            zip(
                [ pos.real, pos.imag, pos.real, pos.imag ],
                [ bounds[0].real, bounds[0].imag, bounds[1].real, bounds[1].imag ],
                [ 1, 1, -1, -1 ]
            )
        )
    )

get_plan_size = lambda plan: ((int(max(map(lambda c: c.real, plan))) + 1), (int(max(map(lambda c: c.imag, plan))) + 1))

get_bounds = lambda plan, tiles: (
    lambda size: [
        0,
        complex(
            size[0] * tiles - 1,
            size[1] * tiles - 1
        )
    ]
)(get_plan_size(plan))


get_risk = lambda plan: (
    lambda size: \
        lambda pos: \
            (plan[complex(int(pos.real) % size[0], int(pos.imag) % size[1])] + int(pos.real) // size[0] + int(pos.imag) // size[1] - 1) % 9 + 1
)(get_plan_size(plan))
    

def path(begin, end, risk, is_out_of_bounds, directions):
    paths = {begin: (0, None)}
    cache = Counter({begin: 0})

    while len(cache) > 0:
        pos, cost = cache.most_common()[-1]
        del cache[pos]

        if pos == end:
            return cost

        start = paths[pos][1]

        updates = functools.reduce(
            lambda acc, update: acc | ({ update[0]: update[1] } if update[0] not in paths or paths[update[0]][0] > update[1][0] else {}),
            map(
                lambda next: (next, (risk(next) + cost, pos)), 
                filter(
                    lambda p: start is None or p != start,
                    itertools.filterfalse(
                        is_out_of_bounds,
                        map(
                            functools.partial(sum, start=pos),
                            map(lambda i: [i], directions)
                        )
                    )
                )
            ),
            {}
        )

        paths |= updates
        cache = Counter(functools.reduce(lambda acc, item: acc | { item[0]: item[1][0] }, updates.items(), cache))

risk = get_risk(plan)

bounds = get_bounds(plan, 1)
print("Part 1:", path(bounds[0], bounds[1], risk, get_is_out_of_bounds(bounds), directions))

bounds = get_bounds(plan, 5)
print("Part 2:", path(bounds[0], bounds[1], risk, get_is_out_of_bounds(bounds), directions))
