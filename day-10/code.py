import collections
import itertools
import functools

chars = { "b": list("(<{["), "e": list(")>}]") }
points1 = { 
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}
points2_order = ")]}>"

def pr(acc, char):
    if isinstance(acc, str):
        return acc
    if len(acc) > 0 and acc[-1] in chars["b"] and char in chars["e"]:
        if chars["b"].index(acc[-1]) == chars["e"].index(char):
            return acc[:-1]
        else:
            return char
    else:
        return acc + [char]

print(
    sum(
        map(
            lambda x: points1[x],
            filter(
                lambda acc: isinstance(acc, str),
                map(
                    lambda line: functools.reduce(
                        pr,
                        list(line),
                        []
                    ),
                    open("input.txt")
                )
            )
        )
    )
)

print(
    next(
        map(
            lambda scores: scores[int(len(scores)/2)], 
            [
                sorted(
                    map(
                        lambda chars: functools.reduce(
                            lambda score, char: score * 5 + (points2_order.index(char) + 1),
                            chars,
                            0
                        ),
                        map(
                            lambda acc: map(
                                lambda c: chars["e"][chars["b"].index(c)], 
                                reversed(acc)
                            ),
                            filter(
                                lambda acc: not isinstance(acc, str),
                                map(
                                    lambda line: functools.reduce(
                                        pr,
                                        list(line.strip()),
                                        []
                                    ),
                                    open("input.txt")
                                )
                            )
                        )
                    )
                )
            ]
        )
    )
)

