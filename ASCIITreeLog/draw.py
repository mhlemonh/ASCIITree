# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from collections import deque
from collections import namedtuple

node_loc = namedtuple("location",["column", "row"])

class PlotBit(object):
    vert = "|"
    vert_right = "├"
    vert_left = "┤"

    hori = "─"
    hori_up = "┴"
    hori_down = "┬"
    
    corner_ur = "┐"
    corner_ul = "┌"
    corner_lr = "┘"
    corner_ll = "└"
    cross = "┼"

class RoundBit(object):
    vert = "|"
    vert_right = "├"
    vert_left = "┤"

    hori = "─"
    hori_up = "┴"
    hori_down = "┬"
    
    corner_ur = "╮"
    corner_ul = "╭"
    corner_lr = "╯"
    corner_ll = "╰"
    cross = "┼"

    @classmethod
    def get_plot_item(cls, t,r,b,l):
        plotitem = {(True, False, True, False):cls.vert,
                    (True, True, True, False):cls.vert_right,
                    (True, False, True, True):cls.vert_left,
                    (False, True, False, True):cls.hori,
                    (True, True, False, True):cls.hori_up,
                    (False, True, True, True):cls.hori_down,
                    (False, False, True, True):cls.corner_ur,
                    (False, True, True, False):cls.corner_ul,
                    (True, False, False, True):cls.corner_lr,
                    (True, True, False, False):cls.corner_ll,
                    (True, True, True, True):cls.cross,
                    (False, False, False, False):" "}
        return plotitem[(t,r,b,l)]

class GraphUtility(object):
    """docstring for GraphUtility"""
    def __init__(self, node_location, time_format, graph_string_spacing=1):
        self.node_location = node_location
        self.max_column = max(node_location[node].column for node in node_location)
        self.content_loc = self.max_column*2+5+len(datetime(1911,10,10).strftime(time_format))
        self.keep_space = graph_string_spacing
        self.flows = {(node_loc(-1,0), node_loc(0,0))} #(up_stream, down_stream, sleep)

    def append_flow(self, from_loc, to_loc):
        self.flows.add((from_loc, to_loc))

    def end_flow(self, column):
        for flow in self.flows:
            if flow[1][0] == column:
                self.flows.remove(flow)
                break

    def __extend_flow(self):
        self.flows = set([(flow[0], flow[1], flow[2]-1) for flow in self.flows])

def show_tree(root_node, node_chr, time_format, plot_element=RoundBit):

    line_struct = "{connection}{keep_space}{time_stamp}{content}".format

    node_list = sort_tree_by_time(root_node)
    node_location = get_column_info(node_list)
    graph_util = GraphUtility(node_location, time_format)
    
    last_column = 0
    tree_unit = []
    for node, node_creat_time in node_list:
        currnet_loc = node_location[node]
        column, row = currnet_loc
        # --- construct connection
        flow_graph = get_conn_graph(row, graph_util, plot_element)
        line_atoms = {"connection":flow_graph,
                      "keep_space":" "*graph_util.keep_space,
                      "time_stamp":" "*len(datetime(2000,1,1).strftime(time_format)),
                      "content": ""}
        tree_unit.append(line_struct(**line_atoms))
        # --- construct node
        flow_graph = get_node_graph(node, node_chr, graph_util, plot_element)
        line_atoms = {"connection":flow_graph,
                      "keep_space":" "*graph_util.keep_space,
                      "time_stamp":node.time.strftime(time_format),
                      "content": " : {}".format(node.name)}
        tree_unit.append(line_struct(**line_atoms))
        # --- upadte graph infos
        graph_util.end_flow(column)

        # --- add flow infomations of childs
        for child in node.downstreams:
            graph_util.append_flow(currnet_loc, node_location[child])

        last_column = column

    return "\n".join(tree_unit)

def get_conn_graph(current_row, graph_utility, plot_element):
    
    raw_atoms = [" " for i in range(graph_utility.max_column*2+1)]
    atoms_bit = [[False, False, False, False] for i in range(graph_utility.max_column*2+1)]

    flow_collection = {}
    for flow in graph_utility.flows:
        fd = flow_collection.get(flow[0], [])
        fd.append(flow[1])
        flow_collection[flow[0]] = fd
    flow_dict = {}
    for from_loc in flow_collection:
        for to_loc in flow_collection[from_loc]:
            if current_row - from_loc[1] == 1:
                fd = flow_dict.get(from_loc[0], set())
                fd.add(to_loc[0])
                flow_dict[from_loc[0]] = fd
            else:
                fd = flow_dict.get(to_loc[0], set())
                fd.add(to_loc[0])
                flow_dict[to_loc[0]] = fd
    for from_col, to_col in flow_dict.items():
        # bit [False, False, False, False] = [Up, Right, Down, Left]
        atoms_bit[from_col*2][0] = True
        for col in to_col:
            atoms_bit[col*2][2] = True
            if col == from_col:
                atoms_bit[col*2][1] = False
                atoms_bit[col*2][3] = False
        if len(to_col) == 1 and from_col != list(to_col)[0]:
            righest_col = max([from_col]+list(to_col))*2
            leftest_col = min([from_col]+list(to_col))*2
            atoms_bit[righest_col][3] = True
            atoms_bit[leftest_col][1] = True
            for col in range(leftest_col+1, righest_col):
                if atoms_bit[col][0] == True and atoms_bit[col][2] == True :
                    continue
                atoms_bit[col][1] = True
                atoms_bit[col][3] = True
        if min(to_col)*2 < max(to_col)*2:
            atoms_bit[min(to_col)*2][1] = True
            atoms_bit[max(to_col)*2][3] = True
        for col in range(min(to_col)*2+1, max(to_col)*2):
            atoms_bit[col][1] = True
            atoms_bit[col][3] = True
    raw_atoms = [RoundBit.get_plot_item(*atom) for atom in atoms_bit]

    return "".join(raw_atoms)

def get_node_graph(node, node_chr, graph_utility, plot_element):
    raw_atoms = [" " for i in range(graph_utility.max_column*2+1)]
    for from_loc, to_loc in graph_utility.flows:
        raw_atoms[to_loc[0]*2] = plot_element.vert
    raw_atoms[graph_utility.node_location[node].column*2] = node_chr
    return "".join(raw_atoms)

def sort_tree_by_time(root_node):
    node = root_node
    queue = deque([])
    traversed_node = set()
    node_list = []
    while True:
        node_list.append((node, node.time))
        traversed_node.add(node)
        # find next node
        if len(queue) == 0 and len(node.downstreams) == 0:
            #finish traversing
            break
        else:
            if len(node.downstreams) != 0:
                next_node = node.downstreams[0]
                queue.extend(node.downstreams[1:])
            else:
                next_node = queue.popleft()
            while next_node in traversed_node:
                next_node = queue.popleft()
        node = next_node
    return sorted(node_list, key=lambda x:x[1])

def get_column_info(node_list):
    column = 0
    row = 0
    location = {None:node_loc(0, 1)}
    last_node = None
    for node_tuple in reversed(node_list):
        row += 1                
        if last_node is None:
            occupied_column = set([0])
        elif have_downstream(node_tuple[0]) and is_oldest_node(node_tuple[0]):        
            childs_occupied_column = [location[node].column for node in node_tuple[0].downstreams]        
            column = min(childs_occupied_column)
            occupied_column = occupied_column.difference(set(childs_occupied_column))
            occupied_column.add(column)        
        else:        
            column = max(occupied_column)+1
            occupied_column.add(column)        
        location[node_tuple[0]] = node_loc(column, len(node_list)-row)
        last_node = node_tuple[0]
    return location

def have_downstream(node):
    return len(node.downstreams) != 0

def is_oldest_node(node):
    result = True
    for c in node.downstreams:
        result = result and all(p.time >= node.time  for p in c.upstreams)
    return result
    
    

if __name__ == '__main__':
    import os
    print os.popen('python /home/raymond/Dropbox/projects/ASCIITree/runtest.py').read()