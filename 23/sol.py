import fileinput
from collections import defaultdict
from itertools import combinations
#import networkx as nx
#import matplotlib.pyplot as plt

#def create_nx_graph(connections, file_name):
#    G = nx.Graph()
#    G.add_edges_from(connections)
#    nx.draw_networkx(G, pos=None, arrows=None, with_labels=True)
#    plt.savefig(file_name)

def parse(connection):
    a, b = connection.split("-")    
    return a, b

def create_graph(connections):
    graph = defaultdict(set)
    nodes = set()
    for a, b in connections:
        graph[a].add(b)
        graph[b].add(a)
        nodes.add(a)
        nodes.add(b)
    return nodes, graph

#def dfs(graph, node, visited):
#    yield node
#    for nn in graph[node]:
#        if nn not in visited:
#            visited.add(nn) 
#            yield from dfs(graph, nn, visited)

#def connected_groups(graph, nodes):
#    groups = []
#    visited = set()
#    for node in nodes:
#        if node not in visited:
#            visited.add(node)
#            groups.append(list(dfs(graph, node, visited)))
#    return groups

def dfs(graph, res, node, path):
    sk = tuple(sorted(path))
    if sk in res:
        return
    res.add(sk)
    for nn in graph[node]:
        if nn in path:
            continue
        if not path <= graph[nn]:
            continue
        path.add(nn)
        dfs(graph, res, nn, path)
        path.discard(nn)

def all_cliques(nodes, graph):
    res = set()
    for node in nodes:
        dfs(graph, res, node, {node})
    return res

connections = [parse(line[:-1]) for line in fileinput.input()]
nodes, graph = create_graph(connections)
cliques = all_cliques(nodes, graph)

# p1
three_cliques = list(clique for clique in cliques if len(clique) == 3)
print(sum(1 for c in three_cliques if any(k[0] == 't' for k in c)))

# p2
print(",".join(sorted(max(cliques, key = len))))
