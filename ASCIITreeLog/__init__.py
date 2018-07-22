import re
import ASCIITreeLog.flow_unit as flow_unit
from ASCIITreeLog.tree import TreeNode
from ASCIITreeLog.draw import show_tree as show_tree_raw

SUPPORT_GRAPH_UNIT = ["connection", "time_stamp", "content"]

def show_tree(root_node,
              node_chr="+",
              time_format="%Y-%m-%d",
              graph_arrangement="{connection}{time_stamp}{content}",
              plot_element=flow_unit.RoundBit):

    # check the inputs
    unsupported_object = "show_tree() method only accept <ASCIITreeLog.TreeNode> object."
    assert isinstance(root_node, TreeNode), unsupported_object

    too_long_charactor_size = "Please use only one character for node symbol."
    assert len(node_chr.decode("utf-8")) == 1, too_long_charactor_size

    unsupported_graph = "graph_arrangement only support {}".format(",".join(SUPPORT_GRAPH_UNIT))
    graph_units = re.compile("/{(/w+)/}").findall(graph_arrangement)
    assert all((unit in SUPPORT_GRAPH_UNIT for unit in graph_units)), unsupported_graph

    # double confirm the node is root
    root_node = root_node.get_root()

    return show_tree_raw(root_node, node_chr, time_format, graph_arrangement, plot_element)
