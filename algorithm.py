import tree
import math
import copy
from collections import deque


class Algorithm:

    def __init__(self, current_tree: tree.Tree):
        self.tree = current_tree
        self.alpha_list = []
        self.tree_list = []

    def print_edges(self):
        for e in self.tree.edges:
            print("Edge score between " + str(e.one.point) + " and "
                  + str(e.other.point) + " is " + str(e.one_to_other_score))
            print("Edge cost between " + str(e.one.point) + " and "
                  + str(e.other.point) + " is " + str(e.one_to_other_cost))
            print("Edge score between " + str(e.other.point) + " and "
                  + str(e.one.point) + " is " + str(e.other_to_one_score))
            print("Edge cost between " + str(e.other.point) + " and "
                  + str(e.one.point) + " is " + str(e.other_to_one_cost))

        return self.tree

    def print_result(self):
        for i in range(len(self.alpha_list)):
            print("alpha = "+ str(self.alpha_list[i]) +
                  " and tree has "+ str(len(self.tree_list[i].nodes)) +" nodes")

        print("Past the last alpha threshold, the tree has " + str(len(self.tree.nodes)) +" node(s).")
    def iterate(self):

        total_score, total_cost = 0, 0

        for node in self.tree.nodes:
            node.score = node.reward
            node.visitOnce = False
            total_score += node.reward

        for edge in self.tree.edges:
            total_cost += edge.cost
            edge.one_to_other_score = 0
            edge.one_to_other_cost = 0
            edge.other_to_one_score = 0
            edge.other_to_one_cost = 0

        stack = deque()  # the order of tracing back
        leaves = self.tree.get_leaves()

        # first level of leaves
        for leaf in leaves:
            stack.append(leaf)
            leaf.visitOnce = True

        leaves = self.tree.get_leaves()
        temp_leaf_count = 0

        # forward
        while len(leaves) != 0:

            temp_leaf_count = len(leaves)
            for leaf in leaves:
                stack.append(leaf)
                leaf.set_score()

            for leaf in leaves:
                leaf.visitOnce = True

            leaves = self.tree.get_leaves()

        # trace back

        min_alpha = math.inf
        min_edge = None

        for edge in self.tree.edges:

            #update score and cost for the other direction
            if len(edge.one.edges) == 1:
                edge.other_to_one_cost = total_cost - edge.cost
                edge.other_to_one_score = total_score - edge.one.score
            elif len(edge.other.edges) == 1:
                edge.one_to_other_cost = total_cost - edge.cost
                edge.one_to_other_score = total_score - edge.other.score
            else:
                if edge.one_to_other_score == 0:
                    edge.one_to_other_score = total_score - edge.other_to_one_score
                    edge.one_to_other_cost = total_cost - edge.cost - edge.other_to_one_cost
                else:
                    edge.other_to_one_score = total_score - edge.one_to_other_score
                    edge.other_to_one_cost = total_cost - edge.cost - edge.one_to_other_cost

            #find minimum alpha and the edge
            if edge.one_to_other_cost != 0:

                if min_alpha > edge.one_to_other_score / edge.one_to_other_cost:
                    min_alpha = edge.one_to_other_score / edge.one_to_other_cost
                    min_edge = edge
            if edge.other_to_one_cost != 0:

                if min_alpha > edge.other_to_one_score / edge.other_to_one_cost:
                    min_alpha = edge.other_to_one_score / edge.other_to_one_cost
                    min_edge = edge

        '''
        if min_edge.one_to_other_cost != 0 and\
                min_alpha == (min_edge.one_to_other_score / min_edge.one_to_other_cost):
            print("min_alpha is " + str(min_alpha) + " and the edge is from "
                  + str(min_edge.one.point) + " to " + str(min_edge.other.point))
        else:
            print("min_alpha is " + str(min_alpha) + " and the edge is from "
                  + str(min_edge.other.point) + " to " + str(min_edge.one.point))
        '''
        if len(self.alpha_list) == 0:
            self.alpha_list.append(min_alpha)
        else:
            self.alpha_list.append(min_alpha+self.alpha_list[-1])
        copied_tree = copy.deepcopy(self.tree)
        self.tree_list.append(copied_tree)

        self.shrink_tree(min_alpha, min_edge)
        #print("Tree has "+ str(len(self.tree.nodes))+ " nodes left")
        #print("Tree has " + str(len(self.tree.edges)) + " edges left")

        #still need to shrink more
        if len(self.tree.nodes) > 2:
            self.tree = self.iterate()
        else:
            self.print_result()
        return self.alpha_list, self.tree_list

    #shrink the tree after increasing alpha
    def shrink_tree(self, alpha, min_edge):

        tree = self.tree
        queue = deque()
        safe_node = None
        if min_edge.one_to_other_cost != 0 and\
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

        for edge in tree.edges:
            edge.one_to_other_score -= alpha * edge.one_to_other_cost
            edge.other_to_one_score -= alpha * edge.other_to_one_cost
        return tree