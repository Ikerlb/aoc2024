from itertools import product
from collections import deque, defaultdict
import fileinput

def parse(grid):
    blocks = set()
    start = end = None
    n, m = len(grid), len(grid[0])
    for r, c in product(range(n), range(m)):
        if grid[r][c] == "S":
            start = (r, c)
        elif grid[r][c] == "E":
            end = (r, c)
    return start, end

def bfs(grid, start):
    q = deque([start])
    dists = {start: 0}
    level = 0
    while q:
        for _ in range(len(q)):
            r, c = q.popleft()
            for nr, nc in neighbors(grid, r, c):
                if grid[nr][nc] != "#" and (nr, nc) not in dists:
                    q.append((nr, nc))
                    dists[(nr, nc)] = level + 1  
        level += 1
    return dists

# credits to deepseek for helping me out xd
def points(grid, r, c, k):
    n, m = len(grid), len(grid[0])
    for dr in range(-k, k + 1):
        rem = k - abs(dr)
        for dc in range(-rem, rem + 1):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m:
                yield (nr, nc, abs(dr) + abs(dc))

def solve(grid, dists, start, area, debug = False):
    n, m = len(grid), len(grid[0])
    res = 0
    for r, c in product(range(n), range(m)):    
        if (r, c) not in dists:
            continue
        for nr, nc, i in points(grid, r, c, area):
            if (nr, nc) in dists:
                diff = dists[(nr, nc)] - dists[(r, c)] - i
                if diff >= 100 and debug:
                    print(f"{i}", diff)
                    print(format(grid,{(r,c,""),(nr,nc,"")}), end = "\n\n")
                if diff >= 100: 
                    res += 1
    return res

def neighbors(grid, r, c):
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        if not (0 <= (nr := r + dr) < len(grid)):
            continue
        if not (0 <= (nc := c + dc) < len(grid)):
            continue
        yield nr, nc

grid = [line[:-1] for line in fileinput.input()]

def part1(grid, start, end): 
    saved = cheats_p1(grid, start, end)

    for k in sorted(k for k in saved):
        cnt = saved[k]
        #print(f"There are {cnt} that save {k} picoseconds.")

    res = 0
    for n, cnt in saved.items():
        if n >= 100:
            res += cnt 

    return res

start, end = parse(grid)
dists = bfs(grid, start)
print(solve(grid, dists, start, 2))
print(solve(grid, dists, start, 20))
