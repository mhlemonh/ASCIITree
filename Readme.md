
ASCIITreeLog
===========

    | 
    + init001
    | 
    + test002
    | 
    + test003
    |\
    | + test002v1
    | |\
    | | + test002v1v1
    | | 
    | + test002v2
    | 
    + test004
    |\
    | + test004v1
    | 
    + test005

Code
====

    import 
    from datetime import datetime
    
    n1 = TreeNode('init001', datetime(2018,3,4), 'content1')
    n2 = TreeNode('test002', datetime(2018,3,5), 'content2')
    n1.add_child(n2)

    n3 = TreeNode('test003', datetime(2018,3,8), 'cont333')
    n2.add_child(n3)

    n4 = TreeNode('test004', datetime(2018,3,30), 'cont333')
    n3.add_child(n4)

    n5 = TreeNode('test005', datetime(2018,4,10), 'cont333')
    n4.add_child(n5)

    b1 = TreeNode('test002v1', datetime(2018,3,12), 'content2')
    b1.set_parent(n2)

    b2 = TreeNode('test002v2', datetime(2018,3,15), 'content2')
    b2.set_parent(b1)

    bb1 = TreeNode('test002v1v1', datetime(2018,3,14), 'content2')
    bb1.set_parent(b1)

    bc1 = TreeNode('test004v1', datetime(2018,4,5), 'content2')
    n4.add_child(bc1)


    draw(b1.get_root())

