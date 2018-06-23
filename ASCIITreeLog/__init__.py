from tree import TreeNode
from draw import show_tree as show_tree_raw

def show_tree(root_node, node_chr="+", time_format="%Y-%m-%d"):
    # control the input file type here
    assert isinstance(root_node, TreeNode), "show_tree() method only accept <ASCIITreeLog.TreeNode> object."
    assert len(node_chr.decode("utf-8")) == 1, "Please use only one character for node symbol."

    root_node = root_node.get_root()

    return show_tree_raw(root_node, node_chr, time_format)