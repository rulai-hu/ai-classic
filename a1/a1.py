
import sys
import re
from functools import reduce
from collections import deque

try:
    import Queue as Q
except ImportError:
    import queue as Q

with open(sys.argv[1], 'r') as file:
    data = file.read()

data = re.findall(r"[\d]+", data)

GRID_SIZE = int(data[0])
print("Grid size =", GRID_SIZE)
START = (int(data[1]), int(data[2]))
GOAL = (int(data[3]), int(data[4]))

GRID = []

for i in range(0, GRID_SIZE):
    GRID.append([])

vals = deque(data[5:])

for row in GRID:
    for j in range(0, GRID_SIZE):
        v = vals.popleft()
        row.append(int(v))

# GRID = [
#     [1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
#     [1, 2, 2, 2, 1, 1, 1, 1, 1, 1],
#     [1, 2, 3, 2, 1, 3, 3, 1, 1, 1],
#     [4, 2, 2, 2, 2, 1, 1, 1, 1, 6],
#     [1, 2, 1, 1, 1, 1, 1, 1, 6, 1],
#     [1, 1, 1, 1, 1, 6, 1, 6, 1, 1],
#     [1, 1, 3, 1, 1, 1, 6, 1, 1, 1],
#     [1, 3, 1, 1, 6, 1, 1, 1, 2, 1],
#     [1, 1, 1, 1, 1, 1, 6, 1, 2, 1],
#     [1, 1, 1, 1, 1, 6, 1, 1, 1, 1]
# ]

def manhattan(src, dst):
    return abs(dst[0] - src[0]) + abs(dst[1] - src[1])

def get_cost(a, b):
    return 1 + abs(GRID[a[1]][a[0]] - GRID[b[1]][b[0]])

def inside_grid(cell):
    x = cell[0]
    y = cell[1]
    return (x >= 0 and y >= 0) and (x < GRID_SIZE and y < GRID_SIZE)

def impassable(cell, nb):
    return (get_cost(cell, nb) - 1) >= 4

def sum_cost(path):
    costs = []
    if len(path) < 2:
        return 0

    for i in range(1, len(path)):
        cost = get_cost(path[i-1], path[i])
        print('adding:', path[i-1], path[i], cost)
        costs.append(cost)

    return reduce(lambda x, y: x + y, costs, 0)

def neighbours(cell):
    x = cell[0]
    y = cell[1]
    result = []

    for nb in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
        if not inside_grid(nb):
            continue

        if impassable(cell, nb):
            continue

        result.append(nb)

    return result

def print_search(expanded, path):
    RES = [['-' for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]

    for cell in expanded:
        x = cell[0]
        y = cell[1]

        RES[y][x] = '='

    for cell in path:
        x = cell[0]
        y = cell[1]

        RES[y][x] = 'X'

    for row in RES:
        print('  '.join(row))

def path_to(parents, goal):
    path = [goal]
    curr = goal
    while curr in parents:
        path.append(parents[curr])
        curr = parents[curr]

    path.reverse()
    return path

def greedy(parents, src, dst):
    if dst == GOAL:
        return 0

    return manhattan(dst, GOAL) + get_cost(src, dst)

def a_star(parents, src, dst):
    path = path_to(parents, dst)
    return sum_cost(path) + greedy(parents, src, dst)

def best_first_search(evaluate):
    current = None
    parents = {}
    closed_list = []
    expanded = { START }
    queue = Q.PriorityQueue()
    queue.put((0, START))

    while not queue.empty() > 0:
        current = queue.get()[1]
        closed_list.append(current)

        if current == GOAL:
            return (expanded, path_to(parents, current))

        nbs = neighbours(current)

        for nb in nbs:
            if nb in closed_list:
                continue

            expanded.add(nb)
            parents[nb] = current
            cost = evaluate(parents, current, nb)
            queue.put((cost, nb))

    return expanded, "FAIL"

#print("\nBest-first Search:")
#expanded, path = best_first_search(greedy)

#if path == "FAIL":
#    print("Search failed!")
#    print_search(expanded, [])
#else:
#    print("Found path to goal from", START, "to", GOAL)
#    print_search(expanded, path)
#    print("Total path cost =", sum_cost(path))
#    print("Expanded nodes =", len(expanded))

print("\nA* Search:")
expanded, path = best_first_search(a_star)

if path == "FAIL":
    print("Search failed!")
    print_search(expanded, [])
else:
    print("Found path to goal from", START, "to", GOAL)
    print_search(expanded, path)
    print("Total path cost =", sum_cost(path))
    print("Expanded nodes =", len(expanded))
