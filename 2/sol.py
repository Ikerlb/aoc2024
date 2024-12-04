from sys import stdin

def parse(line):
    return [int(n) for n in line.split()]

lines = [parse(line[:-1]) for line in stdin]

def is_treshold_ascendent(report, treshold):
    return all(a < b and abs(a - b) < treshold for a, b in zip(report, report[1:]))

def is_safe(report, treshold):
    fst = is_treshold_ascendent(report, treshold)
    snd = is_treshold_ascendent(list(reversed(report)), treshold)
    return fst or snd

def is_safe_p2(report, treshold):
    for i in range(len(report)):
        if is_safe(report[:i] + report[i + 1:], treshold):
            return True
    return is_safe(report, treshold)

def part1(lines):
    return sum(1 for report in lines if is_safe(report, 4))

def part2(lines):
    return sum(1 for report in lines if is_safe_p2(report, 4))

print(f"part 1 is {part1(lines)}")
print(f"part 2 is {part2(lines)}")
