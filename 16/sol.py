from sys import stdin
from heapq import heappush, heappop
from math import inf
from collections import defaultdict

def parse(grid):
    res = set()
    start = end = None
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "S":
                start = (r, c) 
            elif ch == "E":
                end = (r, c) 
            elif ch == "#":
                res.add((r, c))
    return res, start, end

def neighbors(r, c, di):
    yield r + DIRS[di][0], c + DIRS[di][1], di, 1
    ndi = (di + 1) % len(DIRS)
    yield r + DIRS[ndi][0], c + DIRS[ndi][1], ndi, 1001
    pdi = (di - 1) % len(DIRS)
    yield r + DIRS[pdi][0], c + DIRS[pdi][1], pdi, 1001

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

grid = [line[:-1] for line in stdin]            
blocks, start, end = parse(grid)

def retrace(prevs, end_key):
    s = [end_key]
    res = set()
    while s:
        r, c, di = s.pop()
        s.extend(prevs[(r, c, di)])
        res.add((r, c))
    return len(res)

# is this djikstra?
def djikstra(blocks, start, end):
    dists = defaultdict(lambda: inf)
    prevs = defaultdict(list)

    sr, sc = start
    h = [(0, sr, sc, 0)]

    while h:
        w, r, c, di = heappop(h)
        #print(w, r, c, di)
        for nr, nc, ndi, dw in neighbors(r, c, di):
            if (nr, nc) in blocks:
                continue
            nw = w + dw
            if nw < dists[(nr, nc, ndi)]:
                dists[(nr, nc, ndi)] = nw
                prevs[(nr, nc, ndi)] = [(r, c, di)]
                heappush(h, (nw, nr, nc, ndi))
            elif nw == dists[(nr, nc, ndi)]:
                prevs[(nr, nc, ndi)].append((r, c, di))
    return dists, prevs

def part2(blocks, start, end):
    dists, prevs = djikstra(blocks, start, end)
    return retrace(dists, prevs, start, end)

dists, prevs = djikstra(blocks, start, end)
end_key = min((end+(i,) for i in range(len(DIRS))), key = lambda x: dists[x])

# p1
print(dists[end_key])

# p2
print(retrace(prevs, end_key))
