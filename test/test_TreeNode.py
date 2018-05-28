import ASCIITreeLog
import unittest
from datetime import datetime

class TreeNodeTestCase(unittest.TestCase):
    
    def setUp(self):
        self.r0 = ASCIITree.TreeNode('InitNode', datetime(2018,3,4), "I'm the root Node!")
        self.n1 = ASCIITree.TreeNode('Node001', datetime(2018,3,5), 'Root is my parent.')
        self.n2 = ASCIITree.TreeNode('Node002', datetime(2018,3,8), "I'm the children of Node001")
        self.b1 = ASCIITree.TreeNode('Branch001', datetime(2018,3,12), 'Node001 is my parent.')
        self.b2 = ASCIITree.TreeNode('Branch002', datetime(2018,3,15), 'Branch ver.2.')
        self.bb1 = ASCIITree.TreeNode('Branch003', datetime(2018,3,14), 'Child of Branch002')
        self.bc1 = ASCIITree.TreeNode('BB002', datetime(2018,4,5), 'Another child of Branch002')

    def test_set_parent(self):
        self.n1.set_parent(self.r0)
        self.assertTrue(self.n1 in self.r0.childs)
        self.assertEqual(self.n1.parent, self.r0)

    def test_add_child(self):
        self.r0.add_child(self.n1)
        self.assertTrue(self.n1 in self.r0.childs)
        self.assertEqual(self.n1.parent, self.r0)

    def test_get_root(self):
        self.r0.add_child(self.n1)
        self.n1.add_child(self.n2)
        self.b1.set_parent(self.r0)
        self.bb1.set_parent(self.b1)
        self.bc1.set_parent(self.b1)
        self.assertEqual(self.r0.get_root(), self.r0)
        self.assertEqual(self.n1.get_root(), self.r0)
        self.assertEqual(self.n2.get_root(), self.r0)
        self.assertEqual(self.b1.get_root(), self.r0)
        self.assertEqual(self.bb1.get_root(), self.r0)
        self.assertEqual(self.bc1.get_root(), self.r0)


if __name__ == '__main__':
    unittest.main()
