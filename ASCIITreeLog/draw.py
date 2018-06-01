
def show_tree(root_node, node_chr="+", vert_chr="|", branch_chr="|\\", time_format="%Y-%m-%d"):
    sorted_node_list = traverse_tree(root_node)
    column_table, max_column = get_column(sorted_node_list)
    
    last_column = 0
    graph = []
    for node, node_creat_time in sorted_node_list:
        column = column_table[node]
        if last_column < column:
            ascii_connection = (vert_chr+" ")*(column-1)+branch_chr
        else:
            ascii_connection = (vert_chr+" ")*(column+1)
        graph.append("{connections}".format(connections=ascii_connection))
        atoms = {"connection":(vert_chr+" ")*column,
                 "node_chr":node_chr,
                 "keep_space":" "*(max_column-column)*2,
                 "time_stamp":"{}".format(node.time.strftime("%Y-%m-%d")),
                 "content": "{}".format(node.name)}
        graph.append("{connection}{node_chr}{keep_space} {time_stamp} : {content}".format(**atoms))
        last_column = column

    return "\n".join(graph)

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
    column = 0
    max_column = 0
    column_table = {}
    last_node = None
    for node_tuple in reversed(sorted_node_list):
        if last_node == None:
            pass
        elif len(node_tuple[0].childs) != 0:
            column = min([column_table[node]for node in node_tuple[0].childs])
        else:
            column += 1
        column_table[node_tuple[0]] = column
        max_column = column if column > max_column else max_column
        last_node = node_tuple[0]
    return column_table, max_column