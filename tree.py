import sys

class TreeNode:

    def __init__(self, point, r: float, c: float):

        self.point = point
        self.reward = r
        self.cost = c
        self.visitOnce = False
        self.score = r #temporary score
        self.total_cost = c #temporary cost
        self.edges = list()

    def add_edge(self, edge):
        self.edges.append(edge)

    # get node on the other end of the edge
    def get_other_node(self, edge):
        if self == edge.one: return edge.other
        return edge.one

    def get_unvisited_neigbor_count(self):
        count = 0
        for e in self.edges:
            if not self.get_other_node(e).visitOnce:
                count += 1
        return count

    def get_edge(self, otherNode):
        for e in self.edges:
            if self.get_other_node(e) == otherNode:
                return e

        print('Edge not fount, error')
        return None

    def set_score(self):

        for e in self.edges:

            temp_node = self.get_other_node(e)
            if temp_node.visitOnce:
                #for dynamic tree
                e.set_score(temp_node, temp_node.score)
                e.set_cost(temp_node, temp_node.total_cost)
                self.score += temp_node.score
                self.total_cost += temp_node.total_cost


class TreeEdge:

    def __init__(self, one: TreeNode, other: TreeNode):
        self.one = one
        self.other = other
        self.one_to_other_score = 0
        self.one_to_other_cost = 0
        self.other_to_one_score = 0
        self.other_to_one_cost = 0

    def set_score(self, first_node, score):

        if first_node == self.one:
            self.one_to_other_score = score
        else:
            self.other_to_one_score = score

    def set_cost(self,first_node, total_cost):
        if first_node == self.one:
            self.one_to_other_cost = total_cost
        else:
            self.other_to_one_cost = total_cost

    def get_other_node(self, node: TreeNode):
        if node == self.one:
            return self.other
        return self.one



class Tree:

    def __init__(self, points, edgeIndex, reward_list: list, cost_list: list):

        self.nodes = list()
        self.edges = list()

        # index doesn't change
        for i in range(len(points)):
            self.nodes.append(TreeNode(points[i], reward_list[i], reward_list[i] == sys.maxsize))

        for i in range(len(edgeIndex)):
            firstIndex = edgeIndex[i][0]
            secondIndex = edgeIndex[i][1]
            edge = TreeEdge(cost_list[i], self.nodes[firstIndex], self.nodes[secondIndex])
            self.nodes[firstIndex].add_edge(edge)
            self.nodes[secondIndex].add_edge(edge)
            self.edges.append(edge)

    def get_leaves(self):
        leaves_list = list()
        for node in self.nodes:

            if node.visitOnce:
                continue

            if node.get_unvisited_neigbor_count() < 2:
                leaves_list.append(node)

        return leaves_list

    def add_node(self, node: TreeNode):
        self.nodes.append(node)

    def add_edge(self, edge: TreeEdge):
        edge.one.add_edge(edge)
        edge.other.add_edge(edge)
        self.edges.append(edge)

    def __str__(self):

        string = ""

        for node in self.nodes:
            string += ("Node " + str(node.point) + "\'s reward is " + str(node.reward) + "\n")
            string += ("Node " + str(node.point) + "\'s cost is " + str(node.cost) + "\n")

        return string



