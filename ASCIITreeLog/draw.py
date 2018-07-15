# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from collections import deque
from collections import namedtuple

node_loc = namedtuple("location",["column", "row"])

class GraphUtility(object):
    """docstring for GraphUtility"""
    def __init__(self, node_location, time_format, graph_string_spacing=1):
        self.node_location = node_location
        self.max_column = max(node_location[node].column for node in node_location)
        self.keep_space = graph_string_spacing
        self.flows = {(node_loc(-1,0), node_loc(0,0))} #(up_stream, down_stream)

    def append_flow(self, from_loc, to_loc):
        self.flows.add((from_loc, to_loc))

    def end_flow(self, column):
        remove_flows = []
        for flow in self.flows:
            if flow[1].column == column:
                remove_flows.append(flow)
        for rm_flow in remove_flows:
            self.flows.remove(rm_flow)

def show_tree(root_node, node_chr, time_format, graph_arrangement, plot_element):

    line_struct = graph_arrangement.format

    node_list = sort_tree_by_time(root_node)
    node_location = get_column_info(node_list)
    graph_util = GraphUtility(node_location, time_format)
    
    last_column = 0
    tree_unit = []
    for node in node_list:
        currnet_loc = node_location[node]
        # --- construct connection
        flow_graph = get_conn_graph(currnet_loc.row, graph_util, plot_element)
        line_atoms = {"connection":flow_graph+" "*graph_util.keep_space,
                      "time_stamp":" "*len(datetime(2000,1,1).strftime(time_format)),
                      "content": ""}
        tree_unit.append(line_struct(**line_atoms))
        # --- construct node
        flow_graph = get_node_graph(node, node_chr, graph_util, plot_element)
        line_atoms = {"connection":flow_graph+" "*graph_util.keep_space,
                      "time_stamp":node.time.strftime(time_format),
                      "content": " : {}".format(node.name)}
        tree_unit.append(line_struct(**line_atoms))
        # --- upadte graph infos
        graph_util.end_flow(currnet_loc.column)        
        # --- add flow infomations of downstreams
        for stream in node.downstreams:
            graph_util.append_flow(currnet_loc, node_location[stream])

        last_column = currnet_loc.column        
    return "\n".join(tree_unit)

def get_conn_graph(current_row, graph_utility, plot_element):
    flow_graph_bits = [plot_element() for i in range(graph_utility.max_column*2+1)]

    flow_collection = {}
    for flow in graph_utility.flows:
        fd = flow_collection.get(flow[0], [])
        fd.append(flow[1])
        flow_collection[flow[0]] = fd
    flow_dict = {}
    for from_loc in flow_collection:
        for to_loc in flow_collection[from_loc]:
            if current_row - from_loc.row == 1:
                fd = flow_dict.get(from_loc.column, set())
                fd.add(to_loc.column)
                flow_dict[from_loc.column] = fd
            else:
                fd = flow_dict.get(to_loc.column, set())
                fd.add(to_loc.column)
                flow_dict[to_loc.column] = fd    
    for from_col, to_col in flow_dict.items():
        flow_graph_bits[from_col*2].up = True
        for col in to_col:
            flow_graph_bits[col*2].down = True
            if col == from_col:
                flow_graph_bits[col*2].right = False
                flow_graph_bits[col*2].left = False
        if len(to_col) == 1 and from_col != list(to_col)[0]:
            righest_col = max([from_col]+list(to_col))*2
            leftest_col = min([from_col]+list(to_col))*2
            flow_graph_bits[righest_col].left = True
            flow_graph_bits[leftest_col].right = True
            for col in range(leftest_col+1, righest_col):
                if flow_graph_bits[col].up and flow_graph_bits[col].down:
                    continue
                flow_graph_bits[col].right = True
                flow_graph_bits[col].left = True
        if min(to_col)*2 < max(to_col)*2:
            flow_graph_bits[min(to_col)*2].right = True
            flow_graph_bits[max(to_col)*2].left = True
        for col in range(min(to_col)*2+1, max(to_col)*2):
            flow_graph_bits[col].right = True
            flow_graph_bits[col].left = True

    return "".join([atom.get_plot_item() for atom in flow_graph_bits])

def get_node_graph(node, node_chr, graph_utility, plot_element):
    raw_atoms = [" " for i in range(graph_utility.max_column*2+1)]
    for from_loc, to_loc in graph_utility.flows:
        raw_atoms[to_loc.column*2] = plot_element.vert()
    raw_atoms[graph_utility.node_location[node].column*2] = node_chr
    return "".join(raw_atoms)

def sort_tree_by_time(root_node):
    node = root_node
    tracerse_queue = deque([])
    traversed_node = set()
    node_list = []
    while True:
        node_list.append(node)
        traversed_node.add(node)
        # find next node
        if len(tracerse_queue) == 0 and len(node.downstreams) == 0:
            #finish traversing
            break
        else:
            if len(node.downstreams) != 0:
                next_node = node.downstreams[0]
                tracerse_queue.extend(node.downstreams[1:])
            else:
                next_node = tracerse_queue.popleft()
            try:
                while next_node in traversed_node:
                    next_node = tracerse_queue.popleft()
            except IndexError:
                break
        node = next_node
    return sorted(node_list, key=lambda x:x.time)

def get_column_info(node_list):
    column = 0
    row = 0
    location = {None:node_loc(0, 1)}
    last_node = None
    for node in reversed(node_list):
        row += 1                
        if last_node is None:
            occupied_column = set([0])
        elif have_downstream(node) and is_oldest_node(node):        
            childs_occupied_column = [location[downstream_node].column for downstream_node in node.downstreams]        
            column = min(childs_occupied_column)
            occupied_column = occupied_column.difference(set(childs_occupied_column))
            occupied_column.add(column)        
        else:        
            column = max(occupied_column)+1
            occupied_column.add(column)        
        location[node] = node_loc(column, len(node_list)-row)
        last_node = node
    return location

def have_downstream(node):
    return len(node.downstreams) != 0

def is_oldest_node(node):
    result = True
    for c in node.downstreams:
        result = result and all(p.time >= node.time  for p in c.upstreams)
    return result
    
# --- debug functions below ---
    
def __debug_flow_collection(flow_collections):
    print "\n===== flow ====="
    for flow_from in flow_collections:
        for flow_to in flow_collections[flow_from]:
            print "({},{}) -> ({},{})".format(flow_from.column, flow_from.row, flow_to.column, flow_to.row)
    print "================"