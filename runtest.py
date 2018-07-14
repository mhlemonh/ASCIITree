# -*- coding: utf-8 -*-
from ASCIITreeLog import TreeNode, show_tree
from datetime import datetime

n1 = TreeNode('Show', datetime(2018,3,4), 'content1')
n2 = TreeNode('tree graph', datetime(2018,3,5), 'content2')
n1.add_downstream(n2)

n3 = TreeNode('git', datetime(2018,3,30), 'cont333')
n2.add_downstream(n3)

n4 = TreeNode('--graph', datetime(2018,4,10), 'cont333')
n3.add_downstream(n4)

b1 = TreeNode('in', datetime(2018,3,12), 'content2')
b1.set_upstream(n2)

b2 = TreeNode('like', datetime(2018,3,15), 'content2')
b2.set_upstream(n2)
b2.add_downstream(n3)

bb1 = TreeNode('terminal', datetime(2018,3,14), 'content2')
bb1.set_upstream(n2)

bb2 = TreeNode('zzz', datetime(2018,3,16), 'content2')
bb2.set_upstream(bb1)

bc1 = TreeNode('log', datetime(2018,4,5), 'content2')
n3.add_downstream(bc1)

#, "├─┬"
# print show_tree(b1.get_root(), node_chr="★", vert_chr="|", branch_chr="├─┐")
print show_tree(b1.get_root(), node_chr="★", time_format="%Y-%m-%d")
# print show_tree(b1.get_root(), node_chr="★", time_format="%Y-%m-%d")

def print_format_table():
    """
    prints table of formatted text format options
    """
    for style in range(8):
        for fg in range(30,38):
            s1 = ''
            for bg in range(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')

#print_format_table()

# show_tree("ASDDD", node_chr="★", vert_chr="|", branch_chr="├─┐")