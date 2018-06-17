from tree import TreeNode
from draw import show_tree as show_tree_raw
from draw import show_tree2, show_tree3

def show_tree(root_node, node_chr="+", vert_chr="|", branch_chr="|\\ ", time_format="%Y-%m-%d"):
    # control the input file type here
    assert isinstance(root_node, TreeNode), "show_tree() method only accept <ASCIITreeLog.TreeNode> object."
    assert len(node_chr.decode("utf-8")) == 1, "Please use only one character for node symbol."
    assert len(vert_chr.decode("utf-8")) == 1, "Please use only one character for vertical connection symbol."
    assert len(branch_chr.decode("utf-8")) == 3, "Please use three characters for branch connection symbol."

    root_node = root_node.get_root()

    return show_tree_raw(root_node, node_chr, vert_chr, branch_chr, time_format)