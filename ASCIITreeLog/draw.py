def traverse_tree(root_node):
    node = root_node
    queue = []
    node_list = []
    while True:
        node_list.append((node, node.time))

        # find next node
        if len(queue) == 0 and len(node.childs) == 0:
            #finish traversal
            break
        else:
            if len(node.childs) != 0:
                next_node = node.childs[0]
                queue.extend(node.childs[1:])
            else:
                next_node = queue.pop()
        node = next_node
    return sorted(node_list, key=lambda x:x[1])

def get_stage(sorted_node_list):
    stage = 0
    stage_dict = {}
    last_node = None
    for node_tuple in reversed(sorted_node_list):
        if last_node == None:
            pass
        elif len(node_tuple[0].childs) != 0:
            stage = min([stage_dict[node]for node in node_tuple[0].childs])
        else:
            stage += 1
        stage_dict[node_tuple[0]] = stage
        last_node = node_tuple[0]
    return stage_dict

def draw(root_node):
    sorted_node_list = traverse_tree(root_node)
    stage_dict = get_stage(sorted_node_list)
    
    last_stage = 0
    for n in sorted_node_list:
        stage = stage_dict[n[0]]
        if last_stage < stage:
            print "{}|\\".format("| "*(stage-1))
        else:
            print "{}".format("| "*(stage+1))

        print "{}+ {}".format("| "*stage, n[0].name)
        last_stage = stage