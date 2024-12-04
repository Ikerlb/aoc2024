from sys import stdin
from itertools import product

grid = [list(line[:-1]) for line in stdin]

def grid_line(grid, r, c, dr, dc, steps):
    n, m = len(grid), len(grid[0])
    for _ in range(steps):
        if 0 <= r < n and 0 <= c < m:
            yield grid[r][c]
        r += dr
        c += dc

def find(grid, r, c, pattern, dr, dc):
    n, m = len(grid), len(grid[0])
    tgt = "".join(grid_line(grid, r, c, dr, dc, len(pattern)))
    return tgt == pattern or tgt == pattern[::-1]

def find_word(grid, pattern):
    n, m = len(grid), len(grid[0])
    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
    res = 0
    for r, c in product(range(n), range(m)):
        for dr, dc in dirs:
            res += find(grid, r, c, pattern, dr, dc)
    return res

# get grid 3x3 cross
def grid_cross(grid, r, c):
    n, m = len(grid), len(grid[0])
    if r + 2 < n and c + 2 < m:
        center = grid[r + 1][c + 1]
        upper = grid[r][c]+grid[r][c + 2]
        lower = grid[r + 2][c]+grid[r + 2][c + 2]
        return center, [upper, lower]

def find_cross(grid, center, corners):
    n, m = len(grid), len(grid[0])
    res = 0
    for r, c in product(range(n), range(m)):
        if (rr := grid_cross(grid, r, c)) is None:
            continue
        ccen, ccor = rr
        res += (ccor in corners) and (center == ccen)
    return res

def part1(grid):
    return find_word(grid, "XMAS")

def part2(grid):
    corners = [
        ["MS","MS"],
        ["SS","MM"],
        ["SM","SM"],
        ["MM","SS"],
    ]
    center = "A"
    return find_cross(grid, center, corners)

print(part1(grid))
print(part2(grid))
