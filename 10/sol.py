from sys import stdin
from collections import deque, defaultdict
from itertools import product

topo_map = [list(int(c) for c in line[:-1]) for line in stdin]

def neighbors(grid, r, c):
    for dr, dc in [(1,0), (0,1), (-1,0), (0,-1)]:
        if not 0 <= (nr := r + dr) < len(grid):
            continue
        if not 0 <= (nc := c + dc) < len(grid[0]):
            continue
        yield nr, nc

def part1(topo_map):
    q, walked = deque(), defaultdict(set)
    n, m = len(topo_map), len(topo_map[0])
    for r, c in product(range(n), range(m)):
        if topo_map[r][c] == 0:
            q.append((r, c))
            walked[(r, c)].add((r, c))

    for level in range(9):
        for _ in range(len(q)):
            r, c = q.popleft()
            for nr, nc in neighbors(topo_map, r, c):
                if (nr, nc) in walked and topo_map[nr][nc] == level+1:
                    walked[(nr, nc)] |= walked[(r, c)]
                elif topo_map[nr][nc] == level+1:
                    walked[(nr, nc)] |= walked[(r, c)]
                    q.append((nr, nc))
    return sum(len(walked[t]) for t in q)

def part2(topo_map):
    q, walked = deque(), defaultdict(int)
    n, m = len(topo_map), len(topo_map[0])
    for r, c in product(range(n), range(m)):
        if topo_map[r][c] == 0:
            q.append((r, c))
            walked[(r, c)] = 1

    for level in range(9):
        for _ in range(len(q)):
            r, c = q.popleft()
            for nr, nc in neighbors(topo_map, r, c):
                if (nr, nc) in walked and topo_map[nr][nc] == level+1:
                    walked[(nr, nc)] += walked[(r, c)]
                elif topo_map[nr][nc] == level+1:
                    walked[(nr, nc)] += walked[(r, c)]
                    q.append((nr, nc))
    return sum(walked[t] for t in q)

print(part1(topo_map))
print(part2(topo_map))
