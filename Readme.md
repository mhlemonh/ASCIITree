
ASCIITreeLog
===========

#### show tree graph in terminal like "git log --graph"

    | 
    ★     2018-03-04 : Show
    | 
    ★     2018-03-05 : tree graph
    ├─┐
    | ★   2018-03-12 : in
    | | 
    | ★   2018-03-14 : terminal
    | ├─┐
    | | ★ 2018-03-15 : like
    | | 
    | ★   2018-03-24 : terminal2
    | 
    ★     2018-03-30 : git
    ├─┐
    | ★   2018-04-05 : log
    | 
    ★     2018-04-10 : --graph

Code
====

    # -*- coding: utf-8 -*-
    from ASCIITreeLog import TreeNode, show_tree
    from datetime import datetime
    
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
    b2.set_parent(b1)

    bb1 = TreeNode('terminal', datetime(2018,3,14), 'content2')
    bb1.set_parent(b1)

    bc1 = TreeNode('log', datetime(2018,4,5), 'content2')
    n3.add_child(bc1)


    print show_tree(b1.get_root(), node_chr="★", vert_chr="|", branch_chr="├─┐")

