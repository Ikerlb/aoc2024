from sys import stdin

def parse(line):
    fst, snd = line.split(": ")
    return int(fst), [int(n) for n in snd.split(" ")]

equations = [parse(line[:-1]) for line in stdin]

def poss(res, operands, operators):
    def dfs(i):    
        if i == 0:
            return [operands[0]]
        return [op(operands[i], other) for other in dfs(i - 1) for op in operators]
    return res in dfs(len(operands) - 1)

def part1(equations):
    operators = [lambda x, y: x + y, lambda x, y: x * y]
    sm = 0
    for res, operands in equations:
        if poss(res, operands, operators):
            sm += res
    return sm 

def part2(equations):
    operators = [lambda x, y: x + y, lambda x, y: x * y, lambda x, y: int(str(y) + str(x))]
    sm = 0
    for res, operands in equations:
        if poss(res, operands, operators):
            sm += res
    return sm 

print(f"part 1 is {part1(equations)}")
print(f"part 2 is {part2(equations)}")
