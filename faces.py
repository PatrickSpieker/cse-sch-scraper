from ete2 import Tree, TreeNode

list = ["CSE 142", "CSE 143", "CSE 160"]
list_child = ["CSE 311", "CSE 312"]

classes = Tree()
for i in list:
    j = TreeNode(name=i)
    classes.add_child(child=j)
    for k in list_child:
        l = TreeNode(name=k)
        j.add_child(child=l)
        
classes.show()
