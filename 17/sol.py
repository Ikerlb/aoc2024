import re
import fileinput
import z3

class CPU:
    def __init__(self, registers, instructions):
        self.registers = registers
        self.instructions = instructions
        self.pc = 0
    
    def combo(self, operand):
        if 0 <= operand < 4:
            return operand
        elif operand == 4:
            return self.registers["A"]
        elif operand == 5:
            return self.registers["B"]
        elif operand == 5:
            return self.registers["C"]
        else:
            pass

    def __getitem__(self, key):
        return self.registers[key]

    def __setitem__(self, key, val):
        self.registers[key] = val

    def start(self):
        while True:
            if self.pc >= len(self.instructions):
                break
            opcode = self.instructions[self.pc]
            operand = self.instructions[self.pc + 1]
            if (res := self.execute_opcode(opcode, operand)) is not None:
                yield res

    def execute_opcode(self, opcode, operand):
        out = None
        # adv
        if opcode == 0:
            self["A"] = self["A"] // (1 << self.combo(operand))
            #print(f"A <- A // {1 << self.combo(operand)}")
            self.pc += 2
        # bxl
        elif opcode == 1:
            self["B"] = self["B"] ^ operand
            #print(f"B <- B ^ {operand}")
            self.pc += 2
        # bst
        elif opcode == 2:
            self["B"] = self.combo(operand) % 8
            #print(f"B <- {self.combo(operand)} % 8")
            self.pc += 2
        # jnz
        elif opcode == 3:
            self.pc = self.pc + 2 if self["A"] == 0 else operand
        # bxc
        elif opcode == 4:
            self["B"] = self["B"] ^ self["C"]
            #print(f"B <- B ^ C")
            self.pc += 2
        # out
        elif opcode == 5:
            out = self.combo(operand) % 8
            #print(f"OUT <- {self.combo(operand)} % 8")
            self.pc += 2
        # bdv
        elif opcode == 6:
            self["B"] = self["A"] // (1 << self.combo(operand))
            #print(f"B <- A // {1 << self.combo(operand)}")
            self.pc += 2
        # cdv
        else:
            self["C"] = self["A"] // (1 << self.combo(operand))
            #print(f"C <- A // {1 << self.combo(operand)}")
            self.pc += 2
        return out

def parse_register(line):
    r = r'Register ([A-Z]+): (\d+)'
    reg, val = re.match(r, line).groups()
    return reg, int(val)

def parse_instructions(line):
    _, instr = line.split(": ")
    return [int(c) for c in instr.split(",")]

regs, instructions = "".join(fileinput.input()).split("\n\n")
registers = dict(parse_register(line) for line in regs.splitlines())
instructions = parse_instructions(instructions)

def part1(registers, instructions):
    cpu = CPU(registers, instructions)
    return list(cpu.start())

# try solving the problem for 
# output 0, and end A with 0
# real shocker that the response
# is zero hehe
def solve(prev_a, output):
    BV_SIZE = 64

    A = z3.Int('A')
    B1 = z3.BitVec('B1', BV_SIZE)
    B2 = z3.BitVec('B2', BV_SIZE)
    C = z3.Int('C')
    A2 = z3.Int('A2')
    B3 = z3.BitVec('B3', BV_SIZE)
    B4 = z3.BitVec('B4', BV_SIZE)
    TMP = z3.BitVec('TMP', BV_SIZE)
    OUT = z3.Int('OUT')

    # Solver
    s = z3.Solver()
    
    # Constraints
    s.add(z3.BV2Int(B1) == A % 8)
    s.add(B2 == B1 ^ 5)
    s.add(TMP == (1 << B2))
    s.add(z3.BV2Int(B2) >= 0)
    s.add(z3.BV2Int(B2) <= 8)
    s.add(C==(A / z3.BV2Int(TMP)))
    s.add(B3 == B2 ^ z3.Int2BV(C, BV_SIZE))
    s.add(B4 == B3 ^ 6)
    s.add(C >= 0)
    s.add(A >= 0)
    s.add(A2 == A / 8)
    s.add(A2 == prev_a)
    s.add(B4 % 8 == output)

    result = s.check() 
    while result == z3.sat:
        m = s.model()
        a = m[A].as_long()
        yield a
        s.add(A != a)
        result = s.check()

def generate_guess(res):
    start = res[-1] * 8
    while start // 8 == res[-1]:
        yield start
        start += 1

def guess(registers, instructions): 
    def dfs(i, path, res):
        if i < 0:
            res.append(path)
            return
        for prev_a in generate_guess(path):
            regs = {}
            regs["A"] = prev_a
            regs["B"] = 0
            regs["C"] = 0
            cpu = CPU(regs, new_instructions)
            if next(cpu.start()) == instructions[i]:
                dfs(i - 1, path + [prev_a], res)

    # remove 0 that make it loop
    new_instructions = instructions[:-1]
    path = [0]
    res = []
    dfs(len(instructions) - 1 - len(res), path, res)

    # try all possible! (just for curiosity)
    for path in res:
        registers["A"] = path[-1]
        cpu = CPU(registers, instructions)
        assert(list(cpu.start()) == instructions)
    
    return min(path[-1] for path in res)


# p1
print(part1(registers, instructions))

# p2
print(guess(registers, instructions))
