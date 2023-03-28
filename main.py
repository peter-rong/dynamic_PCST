import nodePathGraph
import math
from dynamicTreeAlgorithm import Algorithm

filename = input("Enter file name: ")

file = open(filename, 'r')
lines = file.readlines()
node_count = int(lines[0])
points = []

for i in range(1, node_count +1):
    line = lines[i]
    p1, p2 = float(line.split()[0]), float(line.split()[1])
    points.append([p1,p2])

edge_ids = []
angles = []

for j in range(node_count+2, len(lines)):
    line = lines[j]
    id1, id2, angle = int(line.split()[0]), int(line.split()[1]), float(line.split()[2])
    edge_ids.append([id1,id2])
    angles.append(angle)

initial_graph = nodePathGraph.NodePathGraph(points, edge_ids, angles)
dynamic_tree = initial_graph.to_dynamic_tree_junction()

newAlgo = Algorithm(dynamic_tree)
newAlgo.execute(dynamic_tree)

#outputing file
with open("output.txt", 'w') as f:

    for path in initial_graph.paths:
        f.write(str(newAlgo.tree.nodes[path.TreeNodeIndex].drop_threshold))
        f.write('\n')

f.close()
