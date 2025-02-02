import fileinput
from collections import defaultdict
from functools import lru_cache

def mix(a, b):
    return a ^ b

def prune(a):
    return a % 16777216    

def step1(sn):
    sn = mix(sn, sn * 64)
    return prune(sn)

def step2(sn):
    sn = mix(sn, sn // 32)
    return prune(sn)

def step3(sn):
    sn = mix(sn, sn * 2048)
    return prune(sn)

def next_secret(sn):
    sn = step1(sn)
    sn = step2(sn)
    sn = step3(sn)
    return sn

def gen_secret(sn):
    while True:
        yield sn
        sn = next_secret(sn)

def nth_secret_number(sn, n):
    for _ in range(n):
        sn = next_secret(sn)
    return sn

# did some digging and it looks like
# they are all stuck in the same loop!
# maybe different starts thats all
# pass in an arbitrary number, lets say 1
def gen_all_secret_numbers(start):
    prev = start
    res = [0] * 16777216
    i = 0
    while (sn := next_secret(prev)) != start:
        res[i] = prev
        prev = sn
        i += 1
    res[-1] = prev
    return res

seeds = [int(line[:-1]) for line in fileinput.input()]

def n_secret_numbers(seed, n):
    res = [0 for _ in range(n)]
    sn = seed
    for i in range(n): 
        res[i] = sn
        sn = next_secret(sn)
    return res

def windows(arr, size):
    for i in range(len(arr) - size + 1):
        yield arr[i: i + size]

def reversed_window(arr, size):
    for i in reversed(range(len(arr) - size + 1)):
        yield arr[i: i + size]

def take(gen, n):
    for _, n in zip(range(n), gen):
        yield n

def get_diffs(prices):
    res = [0 for _ in range(len(prices) - 1)]
    #for a, b in zip(prices, prices[1:]):
    for i in range(1, len(prices)):
        am, bm = prices[i - 1] % 10, prices[i] % 10
        res[i - 1] = bm - am, bm
    return res

# first, we want a sequence that
# is shared between all of the seeds
def part2(prices, n):
    s = defaultdict(int)
    for seed in prices:
        nsw = {tuple(fst for fst, _ in w): w[-1][-1] for w in reversed_window(get_diffs(prices[seed]), 4)}
        for w, v in nsw.items():
            s[w] += v
    return max(s.values())

n = 2001
prices = {seed: list(n_secret_numbers(seed, n)) for seed in seeds}

print(sum(l[-1] for l in prices.values()))
print(part2(prices, n))

