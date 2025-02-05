# all credits to deepseek for this!

from graphviz import Digraph
import fileinput
from collections import defaultdict, deque

txt = "".join(fileinput.input())
_, input_text = txt.split("\n\n")

# Create a directed graph
dot = Digraph(comment='Logic Gates Graph')
dot.attr(rankdir='LR')  # Left-to-right layout

# Track nodes by type
output_nodes = set()
input_pairs = {}  # {numeric_id: (x_node, y_node), ...}

lines = input_text.splitlines()
#lines = [line for line in lines if line.split(" ")[1] in ["OR", "XOR"]]
lines = [line for line in lines if line.split(" ")[1] in ["OR", "AND", "XOR"]]


# First pass: Collect nodes and group x/y pairs by numeric ID
for line in lines:
    if not line.strip():
        continue
    lhs, rhs = line.split('->')
    rhs = rhs.strip()
    lhs_parts = lhs.strip().split()
    if len(lhs_parts) != 3:
        continue
    input1, op, input2 = lhs_parts
    # Track output nodes (z**)
    if rhs.startswith('z'):
        output_nodes.add(rhs)
    # Track x/y pairs
    for node in [input1, input2]:
        if node.startswith(('x', 'y')):
            prefix, num = node[0], node[1:]
            numeric_id = int(num)  # Extract numeric ID (e.g., 01, 20)
            if numeric_id not in input_pairs:
                input_pairs[numeric_id] = {'x': None, 'y': None}
            input_pairs[numeric_id][prefix] = node

# Sort pairs by numeric ID (ascending)
sorted_pairs = sorted(input_pairs.items(), key=lambda x: x[0])

# Create ordered list of nodes: x and y grouped by numeric ID (e.g., x01, y01, x03, y03, ...)
sorted_inputs = []
for numeric_id, nodes in sorted_pairs:
    if nodes['x']:
        sorted_inputs.append(nodes['x'])
    if nodes['y']:
        sorted_inputs.append(nodes['y'])

# Sort output nodes (z**) numerically
sorted_z = sorted(output_nodes, key=lambda x: int(x[1:]))

# Add nodes with colors
for node in sorted_inputs:
    if node.startswith('x'):
        dot.node(node, color='blue', style='filled', fillcolor='lightblue')
    elif node.startswith('y'):
        dot.node(node, color='green', style='filled', fillcolor='lightgreen')
for node in sorted_z:
    dot.node(node, color='red', style='filled', fillcolor='#ffcccc')

# Process edges
for line in lines:
    if not line.strip():
        continue
    lhs, rhs = line.split('->')
    rhs = rhs.strip()
    lhs_parts = lhs.strip().split()
    if len(lhs_parts) != 3:
        continue
    input1, op, input2 = lhs_parts
    dot.edge(input1, rhs, label=op)
    dot.edge(input2, rhs, label=op)

# Force vertical ordering for inputs (grouped x/y pairs)
with dot.subgraph(name='inputs') as sub:
    sub.attr(rank='min')  # Place on the far left
    prev_node = None
    for node in sorted_inputs:
        sub.node(node)
        if prev_node:
            sub.edge(prev_node, node, style='invis', weight='10')
        prev_node = node

# Force vertical ordering for outputs (z) on the right
with dot.subgraph(name='outputs') as sub:
    sub.attr(rank='max')  # Place on the far right
    prev_z = None
    for node in sorted_z:
        sub.node(node)
        if prev_z:
            sub.edge(prev_z, node, style='invis', weight='10')
        prev_z = node

# Render and view the graph
dot.render('logic_gates_graph', format='png', view=True)
