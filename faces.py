from ete2 import Tree, TreeNode

list = ["CSE 142", "CSE 143", "CSE 160"]
classes = Tree()
for i in list:
    j = TreeNode(name=i)
    classes.add_child(child=j)
classes.show()
