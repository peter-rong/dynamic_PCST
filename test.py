from tree import Tree, TreeNode, TreeEdge
from algorithm import Algorithm
from randTree import rand_between_bounds, rand_tree

test_tree = rand_tree(1000, [1, 6], [2, 8], 3)
Algorithm(test_tree).execute()
