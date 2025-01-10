from collections import deque, defaultdict
from sys import stdin
from itertools import product

grid = [list(line[:-1]) for line in stdin]

def neighbors(grid, r, c):
    for dr, dc in [(1,0), (0,1), (-1,0), (0,-1)]:
        yield r + dr, c + dc

def neighbors_dirs(grid, r, c):
    for dr, dc in [(1,0), (0,1), (-1,0), (0,-1)]:
        yield r + dr, c + dc, dr, dc

def in_bounds(grid, r, c):
    fst = 0 <= r < len(grid)
    snd = 0 <= c < len(grid[0])
    return fst and snd

def format_grid(grid):
    res = []
    for row in grid:
        res.append("".join(row))
    return "\n".join(res)

def floodfill(grid, r, c):
    target = grid[r][c]
    grid[r][c] = grid[r][c].lower()

    yield r, c
    q = [(r, c)]

    while q:
        r, c = q.pop()
        for nr, nc in neighbors(grid, r, c):
            if not in_bounds(grid, nr, nc):
                continue
            if grid[nr][nc].isupper() and grid[nr][nc] == target:
                q.append((nr, nc))
                yield nr, nc
                grid[nr][nc] = grid[nr][nc].lower()

# boundary_neigh is a map
# of (r, c) -> dirs
def floodfill_dirs(grid, visited, r, c, boundary_neigh, tdr, tdc):
    s = [(r, c)]
    while s: 
        r, c = s.pop()
        for nr, nc in neighbors(grid, r, c):
            if nr < -1 or nr > len(grid) or nc < -1 or nc > len(grid[0]):
                continue
            if (nr, nc) not in boundary_neigh:
                continue
            if (tdr, tdc) not in boundary_neigh[(nr, nc)]:
                continue
            if (nr, nc, tdr, tdc) not in visited:
                visited.add((nr, nc, tdr, tdc))
                s.append((nr, nc))

def get_regions(grid):
     n = len(grid)
     m = len(grid[0])
     regions = []
     for r, c in product(range(n), range(m)):
         if not grid[r][c].islower():
             regions.append(set(floodfill(grid, r, c)))
     return regions 

def format_region(region, n, m):
    s = set(region)
    res = []
    for r in range(n):
        st = "".join("*" if (r, c) in s else "." for c in range(m))
        res.append(st)
    return "\n".join(res)

def valid_neighbors(grid, region, r, c):
    res = []
    for nr, nc in neighbors(grid, r, c):
        if (nr, nc) in region:
            res.append((nr, nc))
    return res

def get_boundary(grid, region):
    boundary = set()
    for r, c in region:
        for nr, nc in neighbors(grid, r, c):
            if not in_bounds(grid, nr, nc) or (nr, nc) not in region:
                boundary.add((r, c))
    return boundary

def perimeter(region):
    return sum(4 - len(valid_neighbors(grid, region, r, c)) for r, c in region)

def area(region):
    return len(region)

def sides(grid, region):
    boundary_neigh = defaultdict(set)
    for r, c in get_boundary(grid, region):
        for nr, nc, dr, dc in neighbors_dirs(grid, r, c):
            if (nr, nc) not in region:
                boundary_neigh[(nr, nc)].add((dr, dc))

    visited = set()
    res = 0
    for tup, dirs in boundary_neigh.items():
        r, c = tup
        for dr, dc in dirs:
            if (r, c, dr, dc) not in visited:
                floodfill_dirs(grid, visited, r, c, boundary_neigh, dr, dc)
                visited.add((r, c, dr, dc))
                res += 1
    return res
    
def part1(grid):
    n, m = len(grid), len(grid[0])
    regions = get_regions(grid)
    res = 0 
    for region in regions:
        res += area(region) * perimeter(region)
        p = perimeter(region)
    return res

def part2(grid):
    n, m = len(grid), len(grid[0])
    regions = get_regions(grid)
    res = 0 
    for region in regions:
        res += area(region) * sides(grid, region)
    return res

# p1
print(part1([row[:] for row in grid]))
# p2
print(part2([row[:] for row in grid]))
