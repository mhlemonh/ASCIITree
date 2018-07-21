# -*- coding: utf-8 -*-

from datetime import datetime
from collections import deque
from collections import namedtuple

NodeCoord = namedtuple("coordinate", ["column", "row"])
NodeLink = namedtuple("link", ["source_node", "destination_node"])

class GraphUtility(object):
    """docstring for GraphUtility"""
    def __init__(self, node_location, time_format, graph_string_spacing=1):
        self.node_location = node_location
        self.max_column = max(node_location[node].column for node in node_location)
        self.keep_space = graph_string_spacing
        self.time_stamp_length = len(datetime(2000, 1, 1).strftime(time_format))
        self.current_renderring_row = -1
        self.links = {NodeLink(NodeCoord(-1, 0), NodeCoord(0, 0))} #(up_stream, down_stream)

    def append_link(self, from_loc, to_loc):
        self.links.add(NodeLink(from_loc, to_loc))

    def end_link(self, column):
        remove_links = []
        for link in self.links:
            if link.destination_node.column == column:
                remove_links.append(link)
        for rm_link in remove_links:
            self.links.remove(rm_link)

    def get_column_link(self):
        link_collection = {}
        for link in self.links:
            destinations = link_collection.get(link.source_node, [])
            destinations.append(link.destination_node)
            link_collection[link.source_node] = destinations

        column_link = {}
        for from_node, to_nodes in link_collection.items():
            for to_node in to_nodes:
                if self.current_renderring_row - from_node.row == 1:
                    to_columns = column_link.get(from_node.column, set())
                    to_columns.add(to_node.column)
                    column_link[from_node.column] = to_columns
                else:
                    to_columns = column_link.get(to_node.column, set())
                    to_columns.add(to_node.column)
                    column_link[to_node.column] = to_columns
        return column_link

def show_tree(root_node, node_chr, time_format, graph_arrangement, plot_element):

    line_struct = graph_arrangement.format

    node_list = sort_node_by_time(root_node)
    node_location = get_node_location(node_list)
    graph_util = GraphUtility(node_location, time_format)

    lines = []
    for node in node_list:
        currnet_loc = node_location[node]
        graph_util.current_renderring_row = currnet_loc.row
        # --- construct connection
        link_graph = get_link_graph(graph_util, plot_element)
        line_atoms = {"connection":link_graph+" "*graph_util.keep_space,
                      "time_stamp":" "*graph_util.time_stamp_length,
                      "content": ""}
        lines.append(line_struct(**line_atoms))
        # --- construct node
        link_graph = get_node_graph(node, node_chr, graph_util, plot_element)
        line_atoms = {"connection":link_graph+" "*graph_util.keep_space,
                      "time_stamp":node.time.strftime(time_format),
                      "content": " : {}".format(node.name)}
        lines.append(line_struct(**line_atoms))
        # --- upadte graph infos
        graph_util.end_link(currnet_loc.column)
        # --- add link infomations of downstreams
        for downstream_node in node.downstreams:
            graph_util.append_link(currnet_loc, node_location[downstream_node])

    return "\n".join(lines)

def get_link_graph(graph_utility, plot_element):
    link_dict = graph_utility.get_column_link()
    link_graph_bits = [plot_element() for _ in range(graph_utility.max_column*2+1)]

    for from_col, to_col in link_dict.items():
        link_graph_bits[from_col*2].up = True
        for col in to_col:
            link_graph_bits[col*2].down = True
            if col == from_col:
                link_graph_bits[col*2].right = False
                link_graph_bits[col*2].left = False
        if len(to_col) == 1 and from_col != list(to_col)[0]:
            righest_col = max([from_col]+list(to_col))*2
            leftest_col = min([from_col]+list(to_col))*2
            link_graph_bits[righest_col].left = True
            link_graph_bits[leftest_col].right = True
            for col in range(leftest_col+1, righest_col):
                if link_graph_bits[col].up and link_graph_bits[col].down:
                    continue
                link_graph_bits[col].right = True
                link_graph_bits[col].left = True
        if min(to_col)*2 < max(to_col)*2:
            link_graph_bits[min(to_col)*2].right = True
            link_graph_bits[max(to_col)*2].left = True
        for col in range(min(to_col)*2+1, max(to_col)*2):
            link_graph_bits[col].right = True
            link_graph_bits[col].left = True

    return "".join([bit.get_plot_item() for bit in link_graph_bits])

def get_node_graph(node, node_chr, graph_utility, plot_element):
    raw_atoms = [" "]*(graph_utility.max_column*2+1)
    for _, to_loc in graph_utility.links:
        raw_atoms[to_loc.column*2] = plot_element.vert()
    raw_atoms[graph_utility.node_location[node].column*2] = node_chr
    return "".join(raw_atoms)

def sort_node_by_time(root_node):
    node = root_node
    traverse_queue = deque([])
    traversed_node = set()
    node_list = []
    while True:
        node_list.append(node)
        traversed_node.add(node)
        # find next node
        if (not traverse_queue) and (not node.downstreams):
            #finish traversing
            break
        else:
            if node.downstreams:
                next_node = node.downstreams[0]
                traverse_queue.extend(node.downstreams[1:])
            else:
                next_node = traverse_queue.popleft()
            try:
                while next_node in traversed_node:
                    next_node = traverse_queue.popleft()
            except IndexError:
                break
        node = next_node
    return sorted(node_list, key=lambda x: x.time)

def get_node_location(node_list):
    row, column = 0, 0
    location = {None:NodeCoord(0, 1)}
    occupied_column = set()
    previous_node = None
    for node in reversed(node_list):
        row += 1
        if previous_node is None:
            column = 0
        elif node.have_downstreams() and node.is_oldest_upstream():
            childs_occupied_column = \
                [location[downstream_node].column for downstream_node in node.downstreams]
            occupied_column = occupied_column.difference(set(childs_occupied_column))
            column = min(childs_occupied_column)
        else:
            column = max(occupied_column)+1

        occupied_column.add(column)
        location[node] = NodeCoord(column, len(node_list)-row)
        previous_node = node
    return location

# --- debug functions below ---

def __debug_link_collection(link_collections):
    print "\n===== link ====="
    for link_from in link_collections:
        for link_to in link_collections[link_from]:
            link_infos = link_from.column, link_from.row, link_to.column, link_to.row
            print "({},{}) -> ({},{})".format(*link_infos)
    print "================"
