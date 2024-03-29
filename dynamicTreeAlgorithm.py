import dynamicTree
import math
import copy
from collections import deque
import time


class Algorithm:

    def __init__(self, current_tree: dynamicTree.DynamicTree):
        self.tree = current_tree.duplicate()
        self.alpha_list = [0]

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

    def execute(self, input_tree):

        # complete component total cost and total score

        start = time.time()

        total_score, total_cost = 0, 0

        for node in input_tree.nodes:
            node.score = node.reward
            node.total_cost = node.cost

            node.visitOnce = False
            total_score += node.reward
            total_cost += node.cost

        for edge in input_tree.edges:
            edge.one_to_other_score = None
            edge.one_to_other_cost = None
            edge.other_to_one_score = None
            edge.other_to_one_cost = None

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

        '''
        for e in input_tree.edges:
            if e.one_to_other_score is None and e.other_to_one_score is None:
                e.one_to_other_score = edge.one.score
                e.one_to_other_cost = edge.one.total_cost

        '''

        # This commented portion is when the input shape is guaranteed to be one connected component

        # corner case of ending with one node
        if len(temp_leaves) == 1:

            temp_node = temp_leaves[0]
            for edge in temp_node.edges:
                if temp_node == edge.one:
                    edge.other_to_one_score = edge.other.score
                    edge.other_to_one_cost = edge.other.total_cost

                else:
                    edge.one_to_other_score = edge.one.score
                    edge.one_to_other_cost = edge.one.total_cost

        if len(temp_leaves) == 2:
            node_one, node_two = temp_leaves[0], temp_leaves[1]

            for edge in node_one.edges:
                if edge.get_other_node(node_one) == node_two:
                    edge.one_to_other_score = edge.one.score
                    edge.one_to_other_cost = edge.one.total_cost

        # trace back
        min_alpha = math.inf
        min_edge = None

        for edge in input_tree.edges:

            if edge.one_to_other_score is None and edge.other_to_one_score is None:
                print("Not Possible")

            elif edge.one_to_other_score is None:
                edge.one_to_other_score = total_score - edge.other_to_one_score
                edge.one_to_other_cost = total_cost - edge.other_to_one_cost

            elif edge.other_to_one_score is None:
                edge.other_to_one_score = total_score - edge.one_to_other_score
                edge.other_to_one_cost = total_cost - edge.one_to_other_cost

            # find minimum alpha and the edge
            if edge.one_to_other_cost != 0 and min_alpha > edge.one_to_other_score / edge.one_to_other_cost:
                min_alpha = edge.one_to_other_score / edge.one_to_other_cost
                min_edge = edge

            if edge.other_to_one_cost != 0 and min_alpha > edge.other_to_one_score / edge.other_to_one_cost:
                min_alpha = edge.other_to_one_score / edge.other_to_one_cost
                min_edge = edge

        # this tree has no edge (is a single node)
        if not min_edge:
            print("This component is a single node.")
            return self.alpha_list

        self.alpha_list.append(min_alpha + self.alpha_list[-1])
        new_tree = self.shrink_tree(input_tree, min_alpha, min_edge)

        iter_counter = 1
        while len(new_tree.edges) > 0:

            iter_counter += 1
            min_alpha = math.inf
            min_edge = None

            for edge in new_tree.edges:

                # find minimum alpha and the edge
                if edge.one_to_other_cost != 0 and min_alpha > edge.one_to_other_score / edge.one_to_other_cost:
                    min_alpha = edge.one_to_other_score / edge.one_to_other_cost
                    min_edge = edge

                if edge.other_to_one_cost != 0 and min_alpha > edge.other_to_one_score / edge.other_to_one_cost:
                    min_alpha = edge.other_to_one_score / edge.other_to_one_cost
                    min_edge = edge

            if not min_edge:
                print("break")
                break

            self.alpha_list.append(min_alpha + self.alpha_list[-1])
            new_tree = self.shrink_tree(new_tree, min_alpha, min_edge)

        end = time.time()
        print("Took " + str(iter_counter) + " iterations")
        print("Time spent: " + str(end - start))

        return self.alpha_list

    # shrink the tree after increasing alpha
    def shrink_tree(self, input_tree, alpha, min_edge):

        total_alpha = self.alpha_list[-1]
        tree = input_tree
        queue = deque()
        min_edge_cost = 0

        safe_node = None

        if not min_edge:
            print("THIS IS NONE")

        if min_edge.one_to_other_cost != 0 and alpha == (min_edge.one_to_other_score / min_edge.one_to_other_cost):
            safe_node = min_edge.other
            queue.append(min_edge.one)
            min_edge_cost = min_edge.one_to_other_cost

        elif min_edge.other_to_one_cost != 0 and alpha == (min_edge.other_to_one_score / min_edge.other_to_one_cost):
            safe_node = min_edge.one
            queue.append(min_edge.other)
            min_edge_cost = min_edge.other_to_one_cost
        else:
            print("Also not possible")

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
            self.tree.nodes[curr_node.index].drop_threshold = total_alpha

        for edge in tree.edges:
            edge.one_to_other_score -= alpha * edge.one_to_other_cost
            edge.other_to_one_score -= alpha * edge.other_to_one_cost

        queue = deque()

        for edge in safe_node.edges:
            queue.append([edge, safe_node])

        while queue:
            curr = queue.popleft()
            curr_edge, curr_node = curr[0], curr[1]

            if curr_node == curr_edge.one:

                curr_edge.one_to_other_cost -= min_edge_cost
                if curr_edge.one_to_other_cost < 0:
                    curr_edge.one_to_other_cost = 0  # amendment from value lost in float point calculation
            elif curr_node == curr_edge.other:
                curr_edge.other_to_one_cost -= min_edge_cost
                if curr_edge.other_to_one_cost < 0:
                    curr_edge.other_to_one_cost = 0  # amendment from value lost in float point calculation
            else:
                print("Also not possible")

            next_node = curr_edge.get_other_node(curr_node)

            for next_edge in next_node.edges:
                if next_edge != curr_edge:
                    queue.append([next_edge, next_node])

        return tree
