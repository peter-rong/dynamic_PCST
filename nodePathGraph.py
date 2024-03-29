from dynamicTree import DynamicTreeNode, DynamicTreeEdge, DynamicTree
from collections import deque
from dynamicTreeAlgorithm import Algorithm
import math


def dist2D(p1, p2):
    return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))


class Node:

    def __init__(self, p):
        self.point = p
        self.isCore = True
        self.paths = set()
        self.index = -1
        self.taken = False

    def et(self):
        return self.bt - self.radius

    def get_one_path(self):
        for p in self.paths:
            return p
        return None

    def add_path(self, path):
        if path not in self.paths:
            self.paths.add(path)

    def remove_path(self, path):
        self.paths.remove(path)

    def is_iso(self):
        return len(self.paths) == 1

    def get_next(self, path):
        return path.other if path.one == self else path.one


class Path:

    def __init__(self, one: Node, other: Node, l: float, angle: float):
        self.one = one
        self.other = other
        self.length = l
        self.theta = angle
        self.isCore = True
        self.inSol = False
        self.TreeNodeIndex = None

        self.pathIndex = None
        self.drop_threshold = None

    def mid_point(self):
        x = (self.one.point[0] + self.other.point[0]) / 2
        y = (self.one.point[1] + self.other.point[1]) / 2
        return [x, y]


class NodePathGraph:

    def __init__(self, points, edges, angle):

        self.nodes = list()
        self.paths = list()

        for pi in range(len(points)):
            newNode = Node(p=points[pi])
            newNode.index = pi
            self.nodes.append(newNode)

        for ei in range(len(edges)):
            e = edges[ei]
            theta = angle[ei]
            pid1 = e[0]
            pid2 = e[1]

            l = dist2D(points[pid1], points[pid2])
            node1 = self.nodes[pid1]
            node2 = self.nodes[pid2]
            path = Path(node1, node2, l, theta)

            node1.add_path(path)
            node2.add_path(path)
            self.paths.append(path)

            path.pathIndex = self.paths.index(path)

        self.burn()

    def burn(self):
        d_ones = self.get_degree_ones()

        queue = deque()

        for n in d_ones:
            queue.append(n)

        while len(queue) > 0:
            targetN = queue.popleft()
            path = targetN.get_one_path()
            if path is None:
                continue

            path.isCore = False
            nextN = targetN.get_next(path)
            nextN.remove_path(path)
            if nextN.is_iso():
                queue.append(nextN)

        self.reset_paths()

    def get_degree_ones(self) -> list():
        ans = list()
        for node in self.nodes:
            if node.is_iso():
                ans.append(node)
        return ans

    def reset_paths(self):
        for path in self.paths:
            path.one.add_path(path)
            path.other.add_path(path)

    def to_components(self):

        graph_list = []

        for node in self.nodes:
            if not node.taken:
                print("print once per component")

                curr_graph = NodePathGraph([], [], [])

                queue = deque()
                queue.append(node)
                node.taken = True

                old_node_list = []
                new_node_list = []
                old_path_list = []

                # BFS to find all connected paths
                while queue:
                    curr_node = queue.popleft()
                    old_node_list.append(curr_node)
                    new_node = Node(curr_node.point)
                    new_node.index = curr_node.index
                    new_node_list.append(new_node)

                    curr_graph.nodes.append(new_node)  # graph level

                    # spread to other nodes

                    for p in curr_node.paths:
                        next_node = curr_node.get_next(p)

                        if not next_node.taken:
                            queue.append(next_node)
                            next_node.taken = True
                            old_path_list.append(p)

                for old_path in old_path_list:
                    old_node_one, old_node_other = old_path.one, old_path.other
                    one_index, other_index = old_node_list.index(old_node_one), old_node_list.index(old_node_other)

                    new_node_one, new_node_other = new_node_list[one_index], new_node_list[other_index]

                    new_path = Path(new_node_one, new_node_other, old_path.length, old_path.theta)
                    new_path.pathIndex = old_path.pathIndex

                    new_node_one.add_path(new_path)
                    new_node_other.add_path(new_path)

                    curr_graph.paths.append(new_path)

                curr_graph.burn()

                graph_list.append(curr_graph)

        return graph_list

    def to_dynamic_tree_junction(self) -> DynamicTree:
        total_reward = 0
        min_cost = math.inf

        dynamicTree = DynamicTree([], [], [], [])

        for node in self.nodes:
            node.isCore = False

        core_nodes = []
        core_node_x = 0
        core_node_y = 0

        for path in self.paths:
            total_reward += (math.sin(path.theta) * path.length)
            min_cost = min(min_cost, path.length)
            if path.isCore:
                path.one.isCore = True
                path.other.isCore = True

                path.TreeNodeIndex = 0

        for node in self.nodes:
            if node.isCore:
                core_nodes.append(node)
                core_node_x += node.point[0]
                core_node_y += node.point[1]

        if len(core_nodes) > 0:
            core_node = DynamicTreeNode([core_node_x / len(core_nodes), core_node_y / len(core_nodes)], total_reward,
                                        min_cost)
            core_node.path_ids = [-1, -1]

            dynamicTree.add_node(core_node)
            core_node.path_index = -2

        path_to_node = {}

        for path in self.paths:
            if not path.isCore:
                new_node = DynamicTreeNode(path.mid_point(), (math.sin(path.theta) * path.length), path.length)

                if path.length == 0:
                    print("path length 0")
                dynamicTree.add_node(new_node)

                new_node.path_index = path.pathIndex

                path.TreeNodeIndex = new_node.index
                path_to_node[path] = new_node

        for node in self.nodes:

            non_core_path = []
            core_count = 0
            for path in node.paths:
                if not path.isCore:
                    non_core_path.append(path)
                else:
                    core_count += 1

            if core_count != 0 and len(non_core_path) < 1:
                continue

            elif core_count != 0 and len(non_core_path) == 1:
                path = non_core_path[0]
                new_edge = DynamicTreeEdge(path_to_node[path], core_node)
                dynamicTree.add_edge(new_edge)

            elif core_count != 0 and len(non_core_path) > 1:
                junction_node = DynamicTreeNode(node.point, 0, 0)
                junction_node.path_ids = [-2, -2]
                dynamicTree.add_node(junction_node)

                new_edge = DynamicTreeEdge(junction_node, core_node)
                dynamicTree.add_edge(new_edge)

                for path in non_core_path:
                    new_edge = DynamicTreeEdge(path_to_node[path], junction_node)
                    dynamicTree.add_edge(new_edge)

            elif core_count == 0 and len(non_core_path) <= 1:
                continue

            elif core_count == 0 and len(non_core_path) == 2:
                path1, path2 = non_core_path[0], non_core_path[1]
                new_edge = DynamicTreeEdge(path_to_node[path1], path_to_node[path2])
                dynamicTree.add_edge(new_edge)

            elif core_count == 0 and len(non_core_path) > 2:
                junction_node = DynamicTreeNode(node.point, 0, 0)
                junction_node.path_ids = [-2, -2]

                dynamicTree.add_node(junction_node)

                for path in non_core_path:
                    new_edge = DynamicTreeEdge(junction_node, path_to_node[path])
                    dynamicTree.add_edge(new_edge)
            else:
                print("impossible")

        return dynamicTree
