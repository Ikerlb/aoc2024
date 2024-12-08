from sys import stdin
from collections import defaultdict, deque

def parse(deps):
    g = defaultdict(list)
    for line in deps.splitlines():
        src, tgt = map(int, line.split("|"))
        g[src].append(tgt)
    return g

def dfs(graph, node, visited, res):
    visited.add(node)
    for nn in graph[node]:
        if nn not in visited:
            dfs(graph, nn, visited, res)
    res.append(node)

def toposort(nodes, graph):
    res = []
    visited = set()
    for n in nodes:
        if n not in visited:
            dfs(graph, n, visited, res)
    return res[::-1]

def fix_updates(graph, path):
    spath = set(path)
    return [n for n in toposort(path, graph) if n in spath]

def is_topo_sorted(g, path):
    indices = {n:i for i, n in enumerate(path)}
    for n in g:     
        for nn in g[n]:
            if (si := indices.get(n, None)) is None:
                continue
            if (ei := indices.get(nn, None)) is None:
                continue
            if si >= ei:
                return False
    return True

txt = "".join(stdin)

fst, snd = txt.split("\n\n")
graph = parse(fst)
paths = [list(map(int, line.split(","))) for line in snd.splitlines()]

def part1(graph, paths):
    return sum(path[len(path) >> 1] for path in paths if is_topo_sorted(graph, path))

def part2(graph, paths):
    res = 0
    for path in paths:
        if is_topo_sorted(graph, path):
            continue
        res += fix_updates(graph, path)[len(path) >> 1]
    return res
    
print(f"part 1 is {part1(graph, paths)}")
print(f"part 2 is {part2(graph, paths)}")
