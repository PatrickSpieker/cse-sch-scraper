from ete2 import Tree, TreeNode, TextFace

list = ["CSE 142", "CSE 143", "CSE 160"]
list_child = ["CSE 311", "CSE 312"]

classes = Tree()
for course in list:
    parent = TreeNode(name=course)
    face = TextFace(text=str(course))
    parent.add_face(face, column=1)
    classes.add_child(child=parent)
    for k in list_child:
        l = TreeNode(name=k)
        parent.add_child(child=l)


classes.show()
