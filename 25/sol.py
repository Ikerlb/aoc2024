from itertools import groupby
import fileinput

def col(grid, c):
    res = [] 
    for r in range(len(grid)):
        res.append(grid[r][c])
    return res

def heights(grid, is_lock):
    res = []
    for c in range(len(grid[0])):
        l = col(grid, c) if is_lock else reversed(col(grid, c))
        _, g = next(groupby(l))
        res.append(len(list(g)) - 1) 
    return res
    
def is_key(grid):
    return all(c == "#" for c in grid[-1])

def is_lock(grid):
    return all(c == "#" for c in grid[0])

def parse(txt):
    grid = [line for line in txt.splitlines()]
    lock = is_lock(grid)
    return "LOCK" if lock else "KEY", heights(grid, lock)

def overlaps(key, lock):
    return any(k + l > 5 for k, l in zip(key, lock))

txt = "".join(fileinput.input())
locks_keys = [parse(t) for t in txt.split("\n\n")]
locks = [hs for t, hs in locks_keys if t == "LOCK"]
keys = [hs for t, hs in locks_keys if t == "KEY"]

res = 0
for i in range(len(keys)):
    for j in range(len(locks)):
        key, lock = keys[i], locks[j]
        #s = "OVERLAPS" if overlaps(key, lock) else "FITS"
        #print(f"checking lock={lock} key={key}, which means it {s}")
        if not overlaps(key, lock):
            res += 1
        

print(res)
