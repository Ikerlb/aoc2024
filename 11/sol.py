from sys import stdin
from functools import lru_cache

txt = "".join(stdin)
stones = [int(n) for n in txt.split(" ")]

def digits(n):
    res = [] if n > 0 else [0]
    while n > 0:
        n, m = divmod(n, 10) 
        res.append(m)
    res.reverse()
    return res

def from_digs(digs):
    res = 0
    for d in digs:
        res = res * 10 + d
    return res

def step(stones):
    nstones = []
    for stone in stones:
        if stone == 0: 
            nstones.append(1)
        elif len(digs := digits(stone)) % 2 == 0:
            half = len(digs) >> 1
            nstones.append(from_digs(digs[:half]))
            nstones.append(from_digs(digs[half:]))
        else:
            nstones.append(stone * 2024)
    return nstones

def steps(stones, n):
    for i in range(n):
        stones = step(stones)
    return stones 

def part1(stones):
    return len(steps(stones, 25))

# in all honesty, i'm not really
# sure what the pattern is...
# i just tried the dp either way
@lru_cache(None)
def dp(n, s):
    if s == 0:
        return 1
    if n == 0:
        return dp(1, s - 1)
    digs = digits(n)
    if len(digs) % 2 == 0:
        half = len(digs) >> 1
        left = dp(from_digs(digs[:half]), s - 1)
        right = dp(from_digs(digs[half:]), s - 1)
        return left + right
    return dp(n * 2024, s - 1)

# try single stones and append them!
# calc number of stones that were
# generated from a single stone
def part2(stones):
    return sum(dp(s, 75) for s in stones)

print(part1(stones))
print(part2(stones))
