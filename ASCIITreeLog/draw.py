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
    branch_chr = brch_right + hori + ur_corner

def show_tree2(root_node, node_chr, time_format):

    sorted_node_list = traverse_tree(root_node)
    column_table, max_column = get_column(sorted_node_list)
    
    last_column = 0
    content_loc = max_column*2+5+len(sorted_node_list[0][0].time.strftime(time_format))
    graph = []
    for node, node_creat_time in sorted_node_list:
        column = column_table[node]
        parent_column = column_table[node.parent]
        __ = " ".join([str(column), str(parent_column), str(last_column)])
        if parent_column == last_column and last_column != column:
            ascii_connection = (ConnASCII.vert+" ")*parent_column+ConnASCII.brch_right+(ConnASCII.hori+ConnASCII.brch_down)*(column-parent_column-1)+ConnASCII.hori+ConnASCII.ur_corner
        elif last_column == column:
            ascii_connection = (ConnASCII.vert+" ")*(column+1)
        elif False:
            pass
        else:
            ascii_connection = (ConnASCII.vert+" ")*(column+1)
        
        connect_atoms = {"connections":ascii_connection,
                         "keep_space":" "*(content_loc-len(ascii_connection.decode('utf-8'))),
                         "detail_info":""}

        graph.append(__ + "{connections}{keep_space}{detail_info}".format(**connect_atoms))

        node_atoms = {"connection":(ConnASCII.vert+" ")*column,
                      "node_chr":node_chr,
                      "keep_space":" "*(max_column-column)*2,
                      "time_stamp":node.time.strftime(time_format),
                      "content": "{}".format(node.name)}
        graph.append("c p l{connection}{node_chr}{keep_space} {time_stamp} : {content}".format(**node_atoms))
        last_column = column

    connect_atoms = {"keep_space":" "*(content_loc),
                     "detail_info":""}
    graph.append("{keep_space}{detail_info}".format(**connect_atoms))

    return "\n".join(graph)

def show_tree3(root_node, node_chr, time_format):

    sorted_node_list = traverse_tree(root_node)
    column_table, max_column = get_column(sorted_node_list)
    
    last_column = 0
    content_loc = max_column*2+5+len(sorted_node_list[0][0].time.strftime(time_format))
    graph = []
    for node, node_creat_time in reversed(sorted_node_list):
        column = column_table[node]

        node_atoms = {"connection":("  ")*column,
                      "node_chr":node_chr,
                      "keep_space":" "*(max_column-column)*2,
                      "time_stamp":node.time.strftime(time_format),
                      "content": "{}".format(node.name)}
        graph.append("{connection}{node_chr}{keep_space} {time_stamp} : {content}".format(**node_atoms))
        last_column = column
    graph.append("|")
    return "\n".join(reversed(graph))

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
    max_column = 0
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
        max_column = column if column > max_column else max_column
        last_node = node_tuple[0]
    return column_table, max_column
