from tree import Tree, TreeNode, TreeEdge
from algorithm import Algorithm

test_tree = Tree([],[],[],[])

node0 = TreeNode(0,1)
node1 = TreeNode(1,2)
node2 = TreeNode(2,2)
node3 = TreeNode(3,3)
node4 = TreeNode(4,4)
node5 = TreeNode(5,5)

edge0 = TreeEdge(-2,node0,node2)
edge1 = TreeEdge(-1,node1,node2)
edge2 = TreeEdge(-4,node2,node3)
edge3 = TreeEdge(-1,node3,node4)
edge4 = TreeEdge(-3,node2,node5)

test_tree.add_node(node0)
test_tree.add_node(node1)
test_tree.add_node(node2)
test_tree.add_node(node3)
test_tree.add_node(node4)
test_tree.add_node(node5)

test_tree.add_edge(edge0)
test_tree.add_edge(edge1)
test_tree.add_edge(edge2)
test_tree.add_edge(edge3)
test_tree.add_edge(edge4)

test_algo = Algorithm(test_tree)

print(test_algo.execute())
