
# ASCIITreeLog

Show tree graph in terminal like "git log --graph" with time series.

![Preview](https://github.com/mhlemonh/ASCIITreeLog/image/screenshot.JPG)

## Installing

```
    git clone https://github.com/mhlemonh/ASCIITreeLog.git
    pip install . 
```
## Example

```python
    # -*- coding: utf-8 -*-
    from ASCIITreeLog import TreeNode, show_tree
    from datetime import datetime
    
    n1 = TreeNode('Show', datetime(2018,3,4), 'foo')
    n2 = TreeNode('tree graph', datetime(2018,3,5), 'bar')
    n1.add_child(n2)

    n3 = TreeNode('git', datetime(2018,3,30), 'foofoo')
    n2.add_child(n3)

    n4 = TreeNode('--graph', datetime(2018,4,10), 'barbar')
    n3.add_child(n4)

    b1 = TreeNode('in', datetime(2018,3,12), 'foobar')
    b1.set_parent(n2)

    b2 = TreeNode('like', datetime(2018,3,15), 'barfoo')
    b2.set_parent(b1)

    bb1 = TreeNode('terminal', datetime(2018,3,14), 'foobarbar')
    bb1.set_parent(b1)

    bc1 = TreeNode('log', datetime(2018,4,5), 'barfoofoo')
    n3.add_child(bc1)


    print show_tree(b1.get_root(), node_chr="★", vert_chr="|", branch_chr="├─┐")
```
