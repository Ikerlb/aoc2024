from sys import stdin
from itertools import product
from collections import defaultdict

def parse_grid(grid):
    gr = gc = None
    mxr = mxc = 0
    obstacles = set()
    for r, c in product(range(len(grid)), range(len(grid[0]))):
        if grid[r][c] == "^":
            gr, gc = r, c
        elif grid[r][c] == "#":
            obstacles.add((r, c))
        mxr = max(r, mxr)
        mxc = max(c, mxc)
    return gr, gc, 0, mxr, 0, mxc, obstacles        

def walk(r, c, dr, dc, obs):
    while (r + dr, c + dc) in obs:
        dr, dc = dc, -dr
    return r + dr, c + dc, dr, dc

def format_dir(dr, dc):
    if (dr, dc) == (-1, 0):
        return "^"
    elif (dr, dc) == (0, -1):
        return "<"
    elif (dr, dc) == (1, 0):
        return "v"
    else:
        return ">"

def format(grid, gr, gc, dr, dc, mnr, mxr, mnc, mxc, obs, visited, turns):
    res = [] 
    for r in range(mnr, mxr + 1):
        row = []
        for c in range(mnc, mxc + 1):
            if (r, c) == (gr, gc):
                row.append(format_dir(dr, dc))
            elif (r, c) in obs:
                row.append("#")
            elif (r, c) in turns:
                row.append("+")
            else:
                row.append(".")
        res.append("".join(row))
    return "\n".join(res)

def walk_till_offbounds(r, c, mnr, mxr, mnc, mxc, obs):
    dr, dc = -1, 0
    visited = defaultdict(set)
    visited[(r, c)].add((dr, dc))
    loops = False

    while True:
        r, c, dr, dc = walk(r, c, dr, dc, obs)
        if not (mnr <= r <= mxr and mnc <= c <= mxc):
            break
        if (r, c) in visited and (dr, dc) in visited[(r, c)]:
            loops = True
            break
        visited[(r, c)].add((dr, dc))
    return visited, loops

def pairs(l):
    for i in range(len(l)):
        for j in range(i + 1, len(l)):
            yield i, j

def part1(r, c, mnr, mxr, mnc, mxc, obs):
    visited, _ = walk_till_offbounds(r, c, mnr, mxr, mnc, mxc, obs)
    return len(visited)

def turn_right_loops(r, c, dr, dc, obs, visited):
    npos = (r + dc, c - dr)
    has_obs = npos in obs
    cycles = npos in visited and (dc, -dr) in visited[npos]
    return has_obs and cycles

def part2(gr, gc, mnr, mxr, mnc, mxc, obs):
    res = 0

    visited, _ = walk_till_offbounds(gr, gc, mnr, mxr, mnc, mxc, obs)

    for pr, pc in visited:
        if (pr, pc) != (gr, gc) and (pr, pc) not in obs: 
            obs.add((pr, pc))
            _, loops = walk_till_offbounds(gr, gc, mnr, mxr, mnc, mxc, obs)
            res += loops
            obs.remove((pr, pc))
    return res


grid = [list(line[:-1]) for line in stdin]
gr, gc, mnr, mxr, mnc, mxc, obs = parse_grid(grid)

print(f"part 1 is {part1(gr, gc, mnr, mxr, mnc, mxc, obs)}")
print(f"part 2 is {part2(gr, gc, mnr, mxr, mnc, mxc, obs)}")
