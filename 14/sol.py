from collections import Counter 
from sys import stdin
import re
import time

ROWS = 103
COLS = 101

class Robot:
    def __init__(self, pr, pc, vr, vc):
        self.pr = pr
        self.pc = pc
        self.vr = vr
        self.vc = vc
        
    def step(self, rows, cols, times):
        self.pr = (self.pr + (self.vr * times)) % rows
        self.pc = (self.pc + (self.vc * times)) % cols

    def __iter__(self):
        yield self.pr
        yield self.pc
        yield self.vr
        yield self.vc

    def clone(self):
        return Robot(*self)

    def quadrant(self, rows, cols):
        mrows = rows >> 1
        mcols = cols >> 1

        if self.pr == mrows or self.pc == mcols:
            return None

        return (int(self.pr > mrows) << 1) + int(self.pc > mcols)

def parse(line):
    r = r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)'
    px, py, vx, vy = map(int, re.match(r, line).groups()) 
    return Robot(py, px, vy, vx)

def format(robots, rows, cols):
    counts = Counter((r.pr, r.pc) for r in robots)
    res = []
    for r in range(rows):
        row = []
        for c in range(cols):
            if (r, c) in counts:
                row.append(str(counts[(r, c)]))
            else:
                row.append(" ")
        res.append("".join(row))
    return "\n".join(res)

# mutates all robots
def step(robots, rows, cols, times = 1):
    for robot in robots:
        robot.step(rows, cols, times)

def part1(robots, rows, cols):
    for _ in range(100):
        step(robots, rows, cols)
    quads = [0 for _ in range(4)]
    for robot in robots:
        if (q := robot.quadrant(rows, cols)) is not None:
            quads[q] += 1
    return quads[0] * quads[1] * quads[2] * quads[3]

# do some trail and error!
# found out that after
# 63 rounds, every rows times
# we get a 'structured'
def part2(robots, rows, cols, times):
    res = 63
    step(robots, rows, cols, times = 63)
    for i in range(times):
        #time.sleep(0.3)
        step(robots, rows, cols, times = rows)
        res += rows
    print(format(robots, rows, cols), end = "\n\n")
    return res


robots = []
for line in stdin:
    robots.append(parse(line))

#step=209085
#step=266939
#step=320353
#step=422969
#step=471637
#step=578990
#step=610235
#step=735329
print(part1([robot.clone() for robot in robots], ROWS, COLS))
print(part2(robots, ROWS, COLS, 60))
