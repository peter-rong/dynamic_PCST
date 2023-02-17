from random import uniform, randint
from tree import TreeNode, TreeEdge, Tree
from algorithm import Algorithm

def rand_between_bounds(bound, sig_fig) -> float:
    lower = bound[0]
    upper = bound[1]

    return round(uniform(lower, upper), sig_fig)


def rand_tree(node_num, cost_bounds, reward_bounds, sig_fig) -> Tree:
    tree = Tree([], [], [], [])

    if node_num == 0:
        return tree

    # first node where no edge can appear
    node_count = 0
    new_node = TreeNode(node_count, rand_between_bounds(reward_bounds, sig_fig))
    tree.nodes.append(new_node)
    node_count += 1
    node_num -= 1

    while node_num != 0:
        old_index = randint(0, node_count - 1)
        old_node = tree.nodes[old_index]
        new_node = TreeNode(node_count, rand_between_bounds(reward_bounds, sig_fig))
        tree.nodes.append(new_node)
        node_count += 1
        node_num -= 1
        new_edge = TreeEdge(rand_between_bounds(cost_bounds, sig_fig), old_node, new_node)
        old_node.edges.append(new_edge)
        new_node.edges.append(new_edge)

        tree.edges.append(new_edge)

    print(tree)
    return tree

test_tree = rand_tree(3, [-3, -1], [0.5, 4], 0)

Algorithm(test_tree).execute()
