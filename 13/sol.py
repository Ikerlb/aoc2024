import re
from sys import stdin

def parse_button(line):
    r = r'Button ([A-Z]+): X+([+-]\d+), Y([+-]\d+)'
    button, x, y = re.match(r, line).groups()
    return button, int(x), int(y)

def parse_prize(line):
    r = r'Prize: X=(\d+), Y=(\d+)'
    x, y = re.match(r, line).groups()
    return int(x), int(y)

def parse(config):
    lines = config.splitlines()
    d = {"Prize": parse_prize(lines[-1])}
    for line in lines[:2]:
        b, x, y = parse_button(line)
        d[b] = (x, y)
    return d

txt = "".join(stdin)
configs = [parse(config) for config in txt.split("\n\n")]

def calc(px, py, ax, ay, bx, by):
    qnum=py*ax - ay*px
    qden=(ax * by) - (ay * bx)

    if qnum % qden != 0:
        return None

    q = qnum // qden
    knum=px - (bx*q)
    kden=ax

    if knum % kden != 0:
        return None
    k = knum // kden
    return (k, q)

def part1(configs):
    res = 0
    for d in configs:
        px, py = d["Prize"]
        ax, ay = d["A"]
        bx, by = d["B"]

        if (tup := calc(px, py, ax, ay, bx, by)) is None:
            continue
        k, q = tup    
        if k > 100 or q > 100:
            continue

        res += 3 * k + q
    return res

def part2(configs):
    res = 0
    for d in configs:
        px, py = map(lambda x: x + 10000000000000, d["Prize"])
        ax, ay = d["A"]
        bx, by = d["B"]

        if (tup := calc(px, py, ax, ay, bx, by)) is None:
            continue
        k, q = tup    

        res += 3 * k + q
    return res
    
print(part1(configs))
print(part2(configs))
