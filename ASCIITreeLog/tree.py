
class TreeNode(object):
    def __init__(self, name, time, docs):
        self.name = name
        self.time = time
        self.docs = docs
        self.childs = []
        self.parent = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return "TreeNode[{}]".format(self.name)

    def add_child(self, child):
        assert isinstance(child, TreeNode), "add_child() method only accept <ASCIITreeLog.TreeNode> object."
        self.childs.append(child)
        if child.parent != self:
            child.set_parent(self)

    def set_parent(self, parent):
        assert isinstance(parent, TreeNode), "set_parent() method only accept <ASCIITreeLog.TreeNode> object."
        assert self.parent is None, "Can not set multiple parent."
        self.parent = parent
        if self not in parent.childs:
            parent.add_child(self)

    def get_root(self):
        if self.parent == None:
            return self
        else:
            return self.parent.get_root()
    