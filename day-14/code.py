import itertools
import functools

from typing import Dict

input_file = "input.txt"

template = next(open(input_file)).strip()
table: Dict = functools.reduce(
    lambda table, rule: table | { rule[0]: rule[1] },
    map(lambda line: line.strip().split(" -> "), itertools.dropwhile(lambda line: "->" not in line, open(input_file))),
    {}
)

update_table = lambda acc, kvp: acc | { kvp[0]: acc.get(kvp[0], 0) + kvp[1] }

@functools.cache
def x(pair, level):
    if level == 0 or pair[1] == " ":
        return { pair[0]: 1  }
    return functools.reduce(
        update_table,
        itertools.chain(
            x(table[pair] + pair[1], level - 1).items(),
            x(pair[0] + table[pair], level - 1).items(),
        ),
        { }
    )

def y(polymer, level):
    return functools.reduce(
        update_table,
        itertools.chain.from_iterable(
            map(
                lambda z: x(z[0] + z[1], level).items(),
                zip(polymer, polymer[1:] + " ")
            )
        ),
        {}
    )

get_result = lambda table: (
    lambda items, key: \
        max(items, key=key)[1] - min(items, key=key)[1]
)(table.items(), lambda kvp: kvp[1])

print(get_result(y(template, 10)))
print(get_result(y(template, 40)))
