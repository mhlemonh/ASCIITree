# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from collections import deque

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

class GraphUtility(object):
    """docstring for GraphUtility"""
    def __init__(self, column_dict, time_format, graph_string_spacing=1):
        self.column_dict = column_dict
        self.max_column = max(column_dict[node] for node in column_dict)
        self.content_loc = self.max_column*2+5+len(datetime(1911,10,10).strftime(time_format))
        self.keep_space = graph_string_spacing
        self.flows = {(0,0)}

    def append_flow(self, from_column, to_columns):
        if isinstance(to_columns, int):
            self.flows.add((from_column, to_columns))
        elif isinstance(to_columns, list):
            for c in to_columns:
                self.flows.add((from_column, c))

    def end_flow(self, column):
        for flow in self.flows:
            if flow[1] == column:
                self.flows.remove(flow)
                break
        self.__extend_flow()

    def __extend_flow(self):
        self.flows = set([(flow[1], flow[1]) for flow in self.flows])

def show_tree(root_node, node_chr, time_format, plot_element=RoundBit):

    line_struct = "{connection}{keep_space}{time_stamp}{content}".format

    node_list = sort_tree_by_time(root_node)
    column_dict = get_column_info(node_list)
    graph_util = GraphUtility(column_dict, time_format)
    
    last_column = 0
    tree_unit = []
    for node, node_creat_time in node_list:
        column = column_dict[node]
        # --- construct connection
        flow_graph = get_conn_graph(node, graph_util, plot_element)
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
        graph_util.append_flow(column, [column_dict[child] for child in node.childs])
        last_column = column

    return "\n".join(tree_unit)

def get_conn_graph(node, graph_utility, plot_element):
    
    raw_atoms = [" " for i in range(graph_utility.max_column*2+1)]

    flow_dict = {}
    for flow in graph_utility.flows:
        fd = flow_dict.get(flow[0], [])
        fd.append(flow[1])
        flow_dict[flow[0]] = sorted(fd)

    for from_col, to_col in flow_dict.items():
        if len(to_col) == 1 and from_col == to_col[0]:
            raw_atoms[from_col*2] = plot_element.vert
        elif len(to_col) > 1:
            # ---
            raw_atoms[min(to_col)*2+1:max(to_col)*2+1] = [plot_element.hori for i in range((max(to_col)-min(to_col))*2)]
            # ---
            if min(to_col) == from_col:
                raw_atoms[from_col*2] = plot_element.vert_right
                raw_atoms[max(to_col)*2] = plot_element.corner_ur
            elif max(to_col) == from_col:
                raw_atoms[from_col*2] = plot_element.corner_ur
                raw_atoms[min(to_col)*2] = plot_element.vert_right
            else:
                raw_atoms[from_col*2] = plot_element.cross
                raw_atoms[min(to_col)*2] = plot_element.corner_ul
                raw_atoms[max(to_col)*2] = plot_element.corner_ur
            # ---
            down_flow_column = set(to_col)
            if from_col in down_flow_column: down_flow_column.remove(from_col)
            if max(to_col) in down_flow_column: down_flow_column.remove(max(to_col))
            if min(to_col) in down_flow_column: down_flow_column.remove(min(to_col))
            for col in down_flow_column:
                raw_atoms[col*2] = plot_element.hori_down
    return "".join(raw_atoms)

def get_node_graph(node, node_chr, graph_utility, plot_element):
    raw_atoms = [" " for i in range(graph_utility.max_column*2+1)]
    for from_column, vert_column in graph_utility.flows:
        raw_atoms[vert_column*2] = plot_element.vert
    raw_atoms[graph_utility.column_dict[node]*2] = node_chr
    return "".join(raw_atoms)

def sort_tree_by_time(root_node):
    node = root_node
    queue = deque([])
    node_list = []
    while True:
        node_list.append((node, node.time))
        # find next node
        if len(queue) == 0 and len(node.childs) == 0:
            #finish traversing
            break
        else:
            if len(node.childs) != 0:
                next_node = node.childs[0]
                queue.extend(node.childs[1:])
            else:
                next_node = queue.popleft()
        node = next_node
    return sorted(node_list, key=lambda x:x[1])

def get_column_info(node_list):
    column = 0
    column_dict = {None:0}
    last_node = None
    for node_tuple in reversed(node_list):
        if last_node == None:
            occupied_column = set([0])
        elif len(node_tuple[0].childs) != 0:
            childs_occupied_column = [column_dict[node]for node in node_tuple[0].childs]
            column = min(childs_occupied_column)
            occupied_column = occupied_column.difference(set(childs_occupied_column))
            occupied_column.add(column)
        else:
            column = max(occupied_column)+1
            occupied_column.add(column)
        column_dict[node_tuple[0]] = column
        last_node = node_tuple[0]
    return column_dict