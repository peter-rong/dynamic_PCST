from tree import Tree, TreeNode, TreeEdge
from algorithm import Algorithm
from randTree import rand_between_bounds, rand_tree

test_tree = rand_tree(10000, [1, 3], [4, 8], 0)
Algorithm(test_tree).iterate()
