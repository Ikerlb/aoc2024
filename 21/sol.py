from collections import deque, defaultdict
from itertools import product
from sys import stdin
from math import inf
from heapq import heappush, heappop
from functools import lru_cache

def neighbors(grid, r, c):
    dirs = {(0,-1): 3, (-1,0): 1, (0,1): 1, (1,0): 2}
    n, m = len(grid), len(grid[0])
    for dr, dc in dirs:
        if not 0 <= (nr := r + dr) < n:
            continue
        if not 0 <= (nc :=c + dc) < m:
            continue
        yield nr, nc, dr, dc, dirs[(dr, dc)]

def neighbors_bfs(grid, r, c):
    dirs = {(0,-1): 3, (-1,0): 1, (0,1): 1, (1,0): 2}
    n, m = len(grid), len(grid[0])
    for dr, dc in dirs:
        if not 0 <= (nr := r + dr) < n:
            continue
        if not 0 <= (nc :=c + dc) < m:
            continue
        yield nr, nc, dr, dc


# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

numpad = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None,"0", "A"],
]

dirpad = [
    [None,"^","A"],
    ["<","v",">"],
]

def generate_grid_pos(pad):
    n, m = len(pad), len(pad[0])
    return {pad[r][c]:(r, c) for r, c in product(range(n), range(m))}

GRIDS = [
    numpad,
    dirpad
]

GRIDS_POS = [generate_grid_pos(pad) for pad in GRIDS]

# a very important
# thing to note here
# is that everytime
# when using the dirpads
# you come back to A

# which means the cost 
# of a move is basically 
# given on the 'upper'
# dirpad's distance from
# that dir to A
# that said, all dirpads
# are the same so we can
# just add weights to the
# directions
def bfs(grid_type, pos, need):
    grid = GRIDS[grid_type]

    r, c = pos
    q = deque([(r, c, "")])
    found = []
    while not found:
        for _ in range(len(q)): 
            r, c, path = q.popleft()
            if (r, c) == need:
                found.append(path + "A")
            for nr, nc, dr, dc in neighbors_bfs(grid, r, c):
                if grid[nr][nc] is not None:
                    q.append((nr, nc, path + format(dr, dc)))
    return found

def reconstruct(prevs, start, end):
    s = [(*end, "A")]
    while s:
        r, c, path = s.pop()
        if (r, c) == start:
            yield path    
            continue
        for pr, pc in prevs[(r, c)]:
            dr, dc = r - pr, c - pc
            s.append((pr, pc, format(dr, dc) + path))
            

def djikstra(grid_type, pos, end):
    grid = GRIDS[grid_type]
    
    r, c = pos
    dists = defaultdict(lambda: inf)
    prevs = defaultdict(list)

    h = [(0, r, c)]

    while h:
        w, r, c = heappop(h)
        #print(w, r, c, di)
        for nr, nc, dr, dc, dw in neighbors(grid, r, c):
            nw = w + dw
            if grid[nr][nc] is not None and nw < dists[(nr, nc)]:
                dists[(nr, nc)] = nw
                prevs[(nr, nc)] = [(r, c)]
                heappush(h, (nw, nr, nc))
            elif nw == dists[(nr, nc)]:
                prevs[(nr, nc)].append((r, c))

    return list(reconstruct(prevs, pos, end))

def char_to_dir(s):
    if s == "^":    
        return -1, 0
    if s == "v":
        return 1, 0
    if s == "<":
        return 0, -1
    if s == ">":
        return 0, 1

def simulate(grid, code):
    n, m = len(grid), len(grid[0])
    pos = {grid[r][c]:(r, c) for r, c in product(range(n), range(m))}
    r, c = pos["A"]
    for ch in code:
        if ch == "A":
            yield grid[r][c]
        else:
            dr, dc = char_to_dir(ch)
            r, c = r + dr, c + dc

def simulate_all(stack, code):
    for grid in reversed(stack):
        code = "".join(simulate(grid, code))    
    return code

def format(dr, dc):
    if (dr, dc) == (0, -1):
        return "<"
    if (dr, dc) == (0, 1):
        return ">"
    if (dr, dc) == (-1, 0):
        return "^"
    if (dr, dc) == (1, 0):
        return "v"
    
def complexity(ln, code):
    num = int("".join(c for c in code if c in "0123456789"))
    return num * ln

@lru_cache(None)
def dp(level, c1, c2, mx):
    if level == mx:
        mn = inf
        #for p in djikstra(0, GRIDS_POS[0][c1], GRIDS_POS[0][c2]):
        for p in bfs(0, GRIDS_POS[0][c1], GRIDS_POS[0][c2]):
            sm = sum(dp(level - 1, cc1, cc2, mx) for cc1, cc2 in zip("A"+p, p))
            mn = min(mn, sm)
        return mn
    if level == 0:
        return len(djikstra(1, GRIDS_POS[1][c1], GRIDS_POS[1][c2])[0])
    mn = inf
    for p in djikstra(1, GRIDS_POS[1][c1], GRIDS_POS[1][c2]):
        sm = sum(dp(level - 1, cc1, cc2, mx) for cc1, cc2 in zip("A"+p, p))
        mn = min(mn, sm)
    return mn


def solve(codes, nums):
    cs = codes[0]
    s = 0
    for code in codes:
        ln = sum(dp(nums, c1, c2, nums) for c1, c2 in zip("A"+code, code))
        s += complexity(ln, code)
    return s

codes = [line[:-1] for line in stdin]
print(solve(codes, 2))
print(solve(codes, 25))
