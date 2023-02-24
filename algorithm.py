import tree
import math
import copy
from collections import deque


class Algorithm:

    def __init__(self, current_tree: tree.Tree):
        self.tree = current_tree
        self.alpha_list = [0]
        self.tree_list = [copy.deepcopy(self.tree)]

    def print_edges(self, input_tree):
        for e in input_tree.edges:
            print("Edge score between " + str(e.one.point) + " and "
                  + str(e.other.point) + " is " + str(e.one_to_other_score))
            print("Edge cost between " + str(e.one.point) + " and "
                  + str(e.other.point) + " is " + str(e.one_to_other_cost))
            print("Edge score between " + str(e.other.point) + " and "
                  + str(e.one.point) + " is " + str(e.other_to_one_score))
            print("Edge cost between " + str(e.other.point) + " and "
                  + str(e.one.point) + " is " + str(e.other_to_one_cost))

    def print_result(self):
        for i in range(len(self.alpha_list)):
            print("alpha = " + str(self.alpha_list[i]) +
                  " and tree has " + str(len(self.tree_list[i].nodes)) + " nodes")

        print("Past the last alpha threshold, the tree has " + str(len(self.tree.nodes)) + " node(s).")

    def execute(self):

        min_alpha, new_tree = self.iterate(self.tree)

        while len(new_tree.edges) > 1:
            min_alpha, new_tree = self.iterate(new_tree)

        self.print_result()

        return self.alpha_list, self.tree_list

    def iterate(self, input_tree):

        total_score, total_cost = 0, 0

        for node in input_tree.nodes:
            node.score = node.reward
            node.visitOnce = False
            total_score += node.reward
            total_cost += node.cost

        for edge in input_tree.edges:
            edge.one_to_other_score = 0
            edge.one_to_other_cost = 0
            edge.other_to_one_score = 0
            edge.other_to_one_cost = 0

        leaves = input_tree.get_leaves()

        # first level of leaves
        for leaf in leaves:
            leaf.visitOnce = True

        leaves = input_tree.get_leaves()
        temp_leaves = leaves

        # forward
        while len(leaves) != 0:

            temp_leaves = leaves
            for leaf in leaves:
                leaf.set_score()

            for leaf in leaves:
                leaf.visitOnce = True

            leaves = input_tree.get_leaves()

        #corner case of ending with one node
        if len(temp_leaves) == 1:

            temp_node = temp_leaves[0]
            for edge in temp_node.edges:
                if temp_node == edge.one:
                    edge.other_to_one_score = edge.other.score
                    edge.other_to_one_cost = edge.other.cost

                else:
                    edge.one_to_other_score = edge.one.score
                    edge.one_to_other_cost = edge.one.cost

        if len(temp_leaves) == 2:
            node_one, node_two = temp_leaves[0], temp_leaves[1]

            for edge in node_one.edges:
                if edge.get_other_node(node_one) == node_two:
                    edge.one_to_other_score = edge.one.score
                    edge.one_to_other_cost = edge.one.cost


        # trace back
        min_alpha = math.inf
        min_edge = None

        for edge in input_tree.edges:

            if edge.one_to_other_score == 0:
                edge.one_to_other_score = total_score - edge.other_to_one_score
                edge.one_to_other_cost = total_cost - edge.other_to_one_cost

            if edge.other_to_one_score == 0:
                edge.other_to_one_score = total_score - edge.one_to_other_score
                edge.other_to_one_cost = total_cost - edge.one_to_other_cost

            # find minimum alpha and the edge
            if min_alpha > edge.one_to_other_score / edge.one_to_other_cost:
                min_alpha = edge.one_to_other_score / edge.one_to_other_cost
                min_edge = edge

            if min_alpha > edge.other_to_one_score / edge.other_to_one_cost:
                min_alpha = edge.other_to_one_score / edge.other_to_one_cost
                min_edge = edge

        self.alpha_list.append(self.alpha_list[-1] + min_alpha)
        new_tree = self.shrink_tree(input_tree, min_alpha, min_edge)
        self.tree_list.append(copy.deepcopy(new_tree))
        print("Tree has "+ str(len(new_tree.nodes))+ " nodes left")

        return min_alpha, new_tree

    # shrink the tree after increasing alpha
    def shrink_tree(self, input_tree, alpha, min_edge):

        tree = input_tree
        queue = deque()
        safe_node = None
        if min_edge.one_to_other_cost != 0 and \
                alpha == (min_edge.one_to_other_score / min_edge.one_to_other_cost):
            safe_node = min_edge.other
            queue.append(min_edge.one)

        else:
            safe_node = min_edge.one
            queue.append(min_edge.other)

        while queue:
            curr_node = queue.popleft()

            for edge in curr_node.edges:

                if edge in tree.edges:

                    tree.edges.remove(edge)

                    other_node = curr_node.get_other_node(edge)

                    if other_node != safe_node:
                        queue.append(other_node)
                    other_node.edges.remove(edge)
            curr_node.edges = []
            tree.nodes.remove(curr_node)

        return tree
