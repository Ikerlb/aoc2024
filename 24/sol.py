import fileinput
from collections import defaultdict, deque
from random import choice 

def parse_bit_input(line):
    idn, val = line.split(": ")
    return idn, int(val)

def parse_operation(line):
    op, tgt = line.split(" -> ")
    op1, operand, op2 = op.split(" ")
    return op1, operand, op2, tgt


txt = "".join(fileinput.input())
fst, snd = txt.split("\n\n")


# mutates state
def _eval(state, op1, operand, op2, tgt):
    funcs = {
        "XOR": lambda x, y: x ^ y,
        "OR": lambda x, y: x | y,
        "AND": lambda x, y: x & y,
    }

    v1 = state[op1]
    v2 = state[op2]
    #print(f"storing into {tgt} {operand}({op1}={v1},{op2}={v2})")
    state[tgt] = funcs[operand](v1, v2)

# mutates state
def eval_all(state, ops):
    for op1, operand, op2, tgt in ops:
        _eval(state, op1, operand, op2, tgt)

    zs = {}
    for k, v in state.items():
        if k[0] == "z":
            zs[int(k[1:])] = v

    res = 0
    for k, v in zs.items(): 
        res |= v << k 
    return res

def graph(ops):
    g = defaultdict(list)
    nodes = set()

    for op1, oper, op2, tgt in ops:
        g[op1].append(tgt)
        g[op2].append(tgt)
        nodes.add(op1)
        nodes.add(op2)
        nodes.add(tgt)

    return nodes, g

# is it a dag?
def toposort(g, nodes):

    incoming = defaultdict(int)

    for frm in g:
        for to in g[frm]:
            incoming[to] += 1

    q = deque([k for k in nodes if incoming[k] == 0])

    res = []
    while q:
        node = q.popleft()
        res.append(node)
        for nn in g[node]:
            incoming[nn] -= 1
            if incoming[nn] == 0:
                q.append(nn)

    if len(res) != len(nodes):
        return None

    return res

def to_bits(n, label, nbits):
    d = {}
    for i in range(nbits):
        d[f"{label}{i:02}"] = (n >> i) & 1
    return d

# assumes topo sorted ops
def solve(ops, x, y):
    sx = to_bits(x, "x", 45)
    sy = to_bits(y, "y", 45)
    sx.update(sy)
    state = sx
    return eval_all(state, ops)

# toposort first, then solve
def solve_with_toposort(ops, x, y):
    nodes, g = graph(ops)
    order = {node:i for i, node in enumerate(toposort(g, nodes))}
    ops = list(sorted(ops, key = lambda item: order[item[-1]]))

    return solve(ops, x, y)

# assumes topo sorted ops
def part1(state, ops):
    state = {k:v for k, v in state.items()}
    return eval_all(state, ops)

def gen_rand(nbits):
    res = 0
    poss = [1,0]
    for i in range(nbits):
        res |= choice(poss) << i
    return res

def inverse(g):
    ng = defaultdict(list)
    for k in g:
        for tgt in g[k]:
            ng[tgt].append(k)
    return ng

# assuming g is the
# inverse graph of g
# also, g is DAG
def backtrack(g, node):
    s = [node]
    res = set()
    while s:
        n = s.pop()
        res.add(n)
        s.extend(g[n])
    return res
    
def test(ops, nums):
    nodes, g = graph(ops)
    if (ts := toposort(g, nodes)) is None:
        return False    
    order = {node:i for i, node in enumerate(ts)}
    ops = list(sorted(ops, key = lambda item: order[item[-1]]))
    for n in range(nums):
        x, y = gen_rand(45), gen_rand(45)
        if (s := solve(ops, x, y)) != x + y: 
            return False
    return True

def ith(n, i):
    return (n >> i) & 1

#("cjb", "OR", "kqr", "z18"),
#("nwg", "AND", "fsf", "z22"),
#("y36", "AND", "x36", "z36"),
#("ffh", "XOR", "gdw", "fvw"),
#("nwg", "XOR", "fsf", "mdb"),
#("svb", "XOR", "fsw", "nwq"),
#def part2(g, state, ops):
#    ig = inverse(g)
#
#    # this took me an
#    # embarrasingly
#    # long time to find
#    possible = [
#
#    ]
#
#    indices = [ops.index(tup) for tup in possible]
#
#
#    for ps in pairs(indices):
#        nops = ops[:]
#        for i, j in ps:
#            nops[i], nops[j] = swap(nops[i], nops[j])
#        if test(nops, 10):
#            return ps
#    return "FAIL"
            
def swap(op1, op2):            
    tgt1, tgt2 = op1[-1], op2[-1]
    nop1 = op1[:-1] + (tgt2,)
    nop2 = op2[:-1] + (tgt1,)
    return nop1, nop2

def pairs(l):
    if len(l) == 2:
        return [[tuple(l)]]
    res = []
    for i in range(len(l)):
        for j in range(i + 1, len(l)):
            rest =  [l[k] for k in range(len(l)) if k not in [i,j]]
            res.extend(p + [(l[i], l[j])] for p in pairs(rest))
    return res    

state = dict(parse_bit_input(line) for line in fst.splitlines())
ops = [parse_operation(line) for line in snd.splitlines()]

nodes, g = graph(ops)

order = {node:i for i, node in enumerate(toposort(g, nodes))}
ops = list(sorted(ops, key = lambda item: order[item[-1]]))
ig = inverse(g)

# p1
print(eval_all({k:v for k, v in state.items()}, ops))

# 
res = [
    "nwq",
    "z36",
    "mdb",
    "z22",
    "fvw",
    "z18",
    "grf",
    "wpq"
]
print(",".join(sorted(res)))
