import collections
import itertools
import functools

brackets = ( "(<{[", ")>}]" )
points1 = { 
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}
points2_order = ")]}>"

def check(acc, char):
    if isinstance(acc, str):
        return acc
    if len(acc) > 0 and acc[-1] in brackets[0] and char in brackets[1]:
        if brackets[0].index(acc[-1]) == brackets[1].index(char):
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
                        check,
                        line.strip(),
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
                                lambda c: brackets[1][brackets[0].index(c)], 
                                reversed(acc)
                            ),
                            filter(
                                lambda acc: not isinstance(acc, str),
                                map(
                                    lambda line: functools.reduce(
                                        check,
                                        line.strip(),
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

