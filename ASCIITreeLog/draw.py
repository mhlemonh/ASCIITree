# -*- coding: utf-8 -*-

import logging

def show_tree(root_node, node_chr, vert_chr, branch_chr, time_format):

    sorted_node_list = traverse_tree(root_node)
    column_table, max_column = get_column(sorted_node_list)
    
    last_column = 0
    content_loc = max_column*2+5+len(sorted_node_list[0][0].time.strftime(time_format))
    graph = []
    for node, node_creat_time in sorted_node_list:
        column = column_table[node]
        if last_column < column:
            ascii_connection = (vert_chr+" ")*(column-1)+branch_chr
        else:
            ascii_connection = (vert_chr+" ")*(column+1)
        
        connect_atoms = {"connections":ascii_connection,
                         "keep_space":" "*(content_loc-len(ascii_connection.decode('utf-8'))),
                         "detail_info":""}

        graph.append("{connections}{keep_space}{detail_info}".format(**connect_atoms))

        node_atoms = {"connection":(vert_chr+" ")*column,
                      "node_chr":node_chr,
                      "keep_space":" "*(max_column-column)*2,
                      "time_stamp":node.time.strftime(time_format),
                      "content": "{}".format(node.name)}
        graph.append("{connection}{node_chr}{keep_space} {time_stamp} : {content}".format(**node_atoms))
        last_column = column

    connect_atoms = {"keep_space":" "*(content_loc),
                     "detail_info":""}
    graph.append("{keep_space}{detail_info}".format(**connect_atoms))

    return "\n".join(graph)

class ConnASCII(object):
    vert = "|"
    hori = "─"
    brch_top = "┴"
    brch_down = "┬"
    brch_right = "├"
    brch_left = "┤"
    ur_corner = "┐"
    ul_corner = "┌"
    lr_corner = "┘"
    ll_corner = "└"
    cross = "┼"
    branch_chr = brch_right + hori + ur_corner

def show_tree3(root_node, node_chr, time_format):

    sorted_node_list = traverse_tree(root_node)
    column_table = get_column(sorted_node_list)
    g_info = graph_infos(column_table, time_format)
    
    last_column = 0
    graph = []
    for node, node_creat_time in sorted_node_list:
        column = column_table[node]

        row = get_conn_graph(node, g_info)

        graph.append(row)

        row = get_node_graph(node, node_chr, g_info)
        g_info.finish_flow(column)
        g_info.add_flow(column, [column_table[child] for child in node.childs])

        node_atoms = {"connection":row,
                      "keep_space":" ",
                      "time_stamp":node.time.strftime(time_format),
                      "content": "{}".format(node.name)}
        graph.append("{connection}{keep_space} {time_stamp} : {content}".format(**node_atoms))
        last_column = column

    return "\n".join(graph)

def get_conn_graph(node, graph_infos):
    
    raw_atoms = [" " for i in range(graph_infos.max_column*2+1)]

    flow_dict = {}
    for flow in graph_infos.flows:
        fd = flow_dict.get(flow[0], [])
        fd.append(flow[1])
        flow_dict[flow[0]] = sorted(fd)
    print flow_dict

    for from_col, to_col in flow_dict.items():
        if len(to_col) == 1 and from_col == to_col[0]:
            raw_atoms[from_col*2] = ConnASCII.vert
        elif len(to_col) > 1:
            if min(to_col) == from_col:
                raw_atoms[from_col*2] = ConnASCII.brch_right
                raw_atoms[max(to_col)*2] = ConnASCII.ur_corner
            elif max(to_col) == from_col:
                raw_atoms[from_col*2] = ConnASCII.ur_corner
                raw_atoms[min(to_col)*2] = ConnASCII.brch_right
            else:
                raw_atoms[from_col*2] = ConnASCII.cross
                raw_atoms[min(to_col)*2] = ConnASCII.ul_corner
                raw_atoms[max(to_col)*2] = ConnASCII.ur_corner
    return "".join(raw_atoms)

def get_node_graph(node, node_chr, graph_infos):
    raw_atoms = [" " for i in range(graph_infos.max_column*2+1)]
    for from_column, vert_column in graph_infos.flows:
        raw_atoms[vert_column*2] = ConnASCII.vert
    raw_atoms[graph_infos.column_table[node]*2] = node_chr
    return "".join(raw_atoms)

class graph_infos(object):
    """docstring for graph_infos"""
    def __init__(self, column_table, time_format):
        self.column_table = column_table
        self.max_column = max(column_table[node] for node in column_table)
        self.content_loc = self.max_column*2+5+len(datetime(1911,10,10).strftime(time_format))
        self.flows = {(0,0)}

    def add_flow(self, from_column, to_columns):
        if isinstance(to_columns, int):
            self.flows.add((from_column, to_columns))
        elif isinstance(to_columns, list):
            for c in to_columns:
                self.flows.add((from_column, c))

    def finish_flow(self, column):
        for flow in self.flows:
            if flow[1] == column:
                self.flows.remove(flow)
                break

        self.flows = set([(flow[1], flow[1]) for flow in self.flows])


    def next_flow(self):
        pass


def traverse_tree(root_node):
    node = root_node
    queue = []
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
                next_node = queue.pop()
        node = next_node
    return sorted(node_list, key=lambda x:x[1])

def get_column(sorted_node_list):
    # TODO: let the column of "in" to be 3
    column = 0
    column_table = {None:0}
    last_node = None
    for node_tuple in reversed(sorted_node_list):
        if last_node == None:
            occupied_column = set([0])
        elif len(node_tuple[0].childs) != 0:
            childs_occupied_column = [column_table[node]for node in node_tuple[0].childs]
            column = min(childs_occupied_column)
            occupied_column = occupied_column.difference(set(childs_occupied_column))
            occupied_column.add(column)
        else:
            column = max(occupied_column)+1
            occupied_column.add(column)
        column_table[node_tuple[0]] = column
        last_node = node_tuple[0]
    return column_table

if __name__ == '__main__':
    from datetime import datetime
    from tree import TreeNode

    n1 = TreeNode('Show', datetime(2018,3,4), 'content1')
    n2 = TreeNode('tree graph', datetime(2018,3,5), 'content2')
    n1.add_child(n2)

    n3 = TreeNode('git', datetime(2018,3,30), 'cont333')
    n2.add_child(n3)

    n4 = TreeNode('--graph', datetime(2018,4,10), 'cont333')
    n3.add_child(n4)

    b1 = TreeNode('in', datetime(2018,3,12), 'content2')
    b1.set_parent(n2)

    b2 = TreeNode('like', datetime(2018,3,15), 'content2')
    b2.set_parent(n2)

    bb1 = TreeNode('terminal', datetime(2018,3,14), 'content2')
    bb1.set_parent(n2)

    bb2 = TreeNode('zzz', datetime(2018,3,16), 'content2')
    bb2.set_parent(bb1)

    bc1 = TreeNode('log', datetime(2018,4,5), 'content2')
    n3.add_child(bc1)

    #, "├─┬"
    # print show_tree(b1.get_root(), node_chr="★", vert_chr="|", branch_chr="├─┐")
    # print show_tree2(b1.get_root(), node_chr="★", time_format="%Y-%m-%d")
    print show_tree3(b1.get_root(), node_chr="★", time_format="%Y-%m-%d")