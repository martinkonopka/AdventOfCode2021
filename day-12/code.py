import functools

file = "sample2.txt"

ends = [ "start", "end" ]

def x(paths, path):
    print(path)

    
    print(paths)
    return paths


paths = functools.reduce(
    lambda paths, path: paths \
        | ({ path[0]: paths.get(path[0], []) + [ path[1] ] } if (path[0] == "start" or path[1] == "end") or (path[0] not in ends and path[1] not in ends) else {}) \
        | ({ path[1]: paths.get(path[1], []) + [ path[0] ] } if (path[1] == "start" or path[0] == "end") or ((path[0] not in ends and path[1] not in ends) and (path[0][0].isupper() or path[1][0].isupper())) else {}),
    map(lambda line: line.strip().split("-"), open(file, "r")), 
    {}
)

check = True
while check:
    check = False
    for start, targets in paths.items():
        for target in targets:
            if (target not in ends) and (target not in paths.keys()):
                check = True
                paths[start].remove(target)

# routes = {} 
# count = 0
# for start, targets in paths.items():


def search(node, paths):
    count = 0
    queue = [ node ]
    path = set()
    while len(queue) > 0:
        current = queue.pop(0)
        
        if current == "end":
            count += 1
        else:
            ways = set(paths[current]).difference(visited)

            queue.extend()
            path.add(current)


print(paths)