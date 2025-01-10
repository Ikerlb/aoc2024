from sys import stdin
from collections import defaultdict, Counter
from itertools import product

grid = [list(line[:-1]) for line in stdin]

def parse(grid):
    antennas = defaultdict(list)
    for r, c in product(range(len(grid)), range(len(grid[0]))):
        if grid[r][c] != ".":
            antennas[grid[r][c]].append((r, c))
    return antennas

def pairs(l):
    for i in range(len(l)):
        for j in range(i + 1, len(l)):
            yield i, j

def bounds(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])

def pair_antinodes(grid, r1, c1, r2, c2, repeat = True):
    dr = r2 - r1
    dc = c2 - c1
    if not repeat:
        if bounds(grid, r2 + dr, c2 + dc):
            yield r2 + dr, c2 + dc
        if bounds(grid, r1 - dr, c1 - dc):
            yield r1 - dr, c1 - dc
    else:
        i = 1
        yield r1, c1
        yield r2, c2
        while bounds(grid, r2 + (i * dr), c2 + (i * dc)):
            yield r2 + (i * dr), c2 + (i * dc)
            i += 1
        i = 1
        while bounds(grid, r1 - (i * dr), c1 - (i * dc)):
            yield r1 - (i * dr), c1 - (i * dc)
            i += 1

# TODO: what if two antennas
# from the same frequency
# create a same antinode?
def antennas_antinodes(grid, coords, part = 1): 
    res = set()
    for i, j in pairs(coords):
        r1, c1 = coords[i]
        r2, c2 = coords[j]
        if part == 1:
            res.update(pair_antinodes(grid, r1, c1, r2, c2, repeat = False))
        else:
            res.update(pair_antinodes(grid, r1, c1, r2, c2, repeat = True))
    return res

def format(grid, antinodes):
    rev_ant = {coord:a for a, coords in antennas.items() for coord in coords}
    res = []
    for r in range(len(grid)):
        row = []
        for c in range(len(grid[0])):
            if (r, c) in antinodes:
                row.append("#")
            elif grid[r][c] != ".":
                row.append(grid[r][c])
            else:
                row.append(".")
        res.append("".join(row))
    return "\n".join(res)

antennas = parse(grid)

def part1(grid, antennas):
    anns = set()
    for antenna, coords in antennas.items():
        anns.update(antennas_antinodes(grid, coords, part = 1))
    return len(anns)

def part2(grid, antennas):
    anns = set()
    for antenna, coords in antennas.items():
        anns.update(antennas_antinodes(grid, coords, part = 2))
    return len(anns)

print(f"part 1 is {part1(grid, antennas)}")
print(f"part 2 is {part2(grid, antennas)}")
