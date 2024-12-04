from sys import stdin
import re

text = "".join(stdin)

def part1(text):
    regex = r"mul\(\d{1,3},\d{1,3}\)"
    matches = [m for m in re.finditer(regex, text, re.MULTILINE)]
    s = 0
    for m in matches:
        a, b = map(int, m.group()[4:-1].split(","))
        s += a * b
    return s

def part2(text):
    regex = r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)"
    matches = [m for m in re.finditer(regex, text, re.MULTILINE)]
    on = True
    s = 0
    for m in matches:
        instr = m.group()
        if instr == "do()":
            on = True
        elif instr == "don't()":
            on = False
        else:
            a, b = map(int, instr[4:-1].split(","))
            s += on * a * b
    return s

print(f"part 1 is {part1(text)}")
print(f"part 2 is {part2(text)}")

