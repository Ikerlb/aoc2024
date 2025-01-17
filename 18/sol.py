import fileinput
from itertools import product
from collections import deque

#N, M, BYTES = 7, 7, 12
N, M, BYTES = 71, 71, 1024

def parse(line):
    c, r = map(int, line.split(","))
    return r, c 

def construct(coords, n, m):
    grid = [[None for _ in range(m)] for _ in range(n)]
    for r, c in coords:
        grid[r][c] = "#"
    return grid

def format(grid):
    res = []
    for row in grid:
        res.append("".join("." if c is None else c for c in row))
    return "\n".join(res)

def neighbors(grid, r, c):
    for dr, dc in [(0,-1), (-1,0), (1,0), (0,1)]:
        nr, nc = r + dr, c + dc
        if not 0 <= nr < len(grid):
            continue
        if not 0 <= nc < len(grid[0]):
            continue
        yield nr, nc

# i also feel like I can
# do Union Find Set
# in much better time
# complexity
def bfs(grid, start, end):
    q = deque([start])
    visited = {start}
    level = 0
    while q:
        for _ in range(len(q)):
            r, c = q.popleft()
            if (r, c) == end:
                return level
            for nr, nc in neighbors(grid, r, c):
                if grid[nr][nc] is None and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    q.append((nr, nc))
        level += 1
    return None

def part1(coords, n, m, num_bytes):
    grid = construct(coords[:num_bytes], n, m)
    #print(format(grid))
    start = (0, 0)
    end = (n - 1, m - 1)
    return bfs(grid, start, end)

# is it better than iterating
# until you can't who knows...
def part2(coords, n, m):
    start = (0, 0)
    start = (0, 0)
    end = (n - 1, m - 1)

    l, r = 0, len(coords) - 1
    res = 0
    while l <= r:
        mid = (l + r) >> 1
        if bfs(construct(coords[:mid], n, m), start, end) is not None:
            l = mid + 1
            res = mid
        else:
            r = mid - 1
    r, c = coords[res]
    return f"{c},{r}"

coords = [parse(line) for line in fileinput.input()]
print(part1(coords, N, M, BYTES))
print(part2(coords, N, M))
