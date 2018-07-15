
class TreeNode(object):
    def __init__(self, name, time, docs=""):
        self.name = name
        self.time = time
        self.docs = docs
        self.downstreams = []
        self.upstreams = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return "TreeNode[{}]".format(self.name)

    def __eq__(self, other):
        return (self.name == other.name) and (self.time == other.time)

    def __ne__(self, other):
        return not self.__eq__(other)

    def add_downstream(self, node):
        assert isinstance(node, TreeNode), "add_downstream() method only accept <ASCIITreeLog.TreeNode> object."
        self.downstreams.append(node)
        if self not in node.upstreams:
            node.set_upstream(self)

    def set_upstream(self, node):
        assert isinstance(node, TreeNode), "set_upstream() method only accept <ASCIITreeLog.TreeNode> object."
        self.upstreams.append(node)
        if self not in node.downstreams:
            node.add_downstream(self)

    def get_root(self):
        if len(self.upstreams) == 0:
            return self
        else:
            return self.upstreams[0].get_root()
    