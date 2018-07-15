# -*- coding: utf-8 -*-

import ASCIITreeLog
import unittest
from datetime import datetime

class TreeNodeTestCase(unittest.TestCase):
    
    def setUp(self):
        self.r0 = ASCIITreeLog.TreeNode('InitNode', datetime(2018,3,4), "I'm the root Node!")
        self.n1 = ASCIITreeLog.TreeNode('Node001', datetime(2018,3,5), 'Root is my parent.')
        self.n2 = ASCIITreeLog.TreeNode('Node002', datetime(2018,3,8), "I'm the children of Node001")
        self.b1 = ASCIITreeLog.TreeNode('Branch001', datetime(2018,3,12), 'Node001 is my parent.')
        self.b2 = ASCIITreeLog.TreeNode('Branch002', datetime(2018,3,15), 'Branch ver.2.')
        self.bb1 = ASCIITreeLog.TreeNode('Branch003', datetime(2018,3,14), 'Child of Branch002')
        self.bc1 = ASCIITreeLog.TreeNode('BB002', datetime(2018,4,5), 'Another child of Branch002')

    def test_set_parent(self):
        self.n1.set_upstream(self.r0)
        self.assertTrue(self.n1 in self.r0.downstreams)
        self.assertTrue(self.r0 in self.n1.upstreams)

    def test_add_child(self):
        self.r0.add_downstream(self.n1)
        self.assertTrue(self.n1 in self.r0.downstreams)
        self.assertTrue(self.r0 in self.n1.upstreams)

    def test_get_root(self):
        self.r0.add_downstream(self.n1)
        self.n1.add_downstream(self.n2)
        self.b1.set_upstream(self.r0)
        self.bb1.set_upstream(self.b1)
        self.bc1.set_upstream(self.b1)
        self.assertEqual(self.r0.get_root(), self.r0)
        self.assertEqual(self.n1.get_root(), self.r0)
        self.assertEqual(self.n2.get_root(), self.r0)
        self.assertEqual(self.b1.get_root(), self.r0)
        self.assertEqual(self.bb1.get_root(), self.r0)
        self.assertEqual(self.bc1.get_root(), self.r0)

class DrawTestCase(unittest.TestCase):

    def setUp(self):
        self.r0 = ASCIITreeLog.TreeNode('InitNode', datetime(2018,3,4), "I'm the root Node!")
        self.n1 = ASCIITreeLog.TreeNode('Node001', datetime(2018,3,5), 'Root is my parent.')
        self.n2 = ASCIITreeLog.TreeNode('Node002', datetime(2018,3,8), "I'm the children of Node001")
        self.b1 = ASCIITreeLog.TreeNode('Branch001', datetime(2018,3,12), 'Node001 is my parent.')
        self.b2 = ASCIITreeLog.TreeNode('Branch002', datetime(2018,3,15), 'Branch ver.2.')
        self.bb1 = ASCIITreeLog.TreeNode('Branch003', datetime(2018,3,14), 'Child of Branch002')
        self.bc1 = ASCIITreeLog.TreeNode('BB002', datetime(2018,4,5), 'Another child of Branch002')
    
    def test_simple_branch(self):
        self.r0.add_downstream(self.n1)
        self.r0.add_downstream(self.n2)
        expected_graph=("|   \n"
                        "+   \n"
                        "├─╮ \n"
                        "| + \n"
                        "|   \n"
                        "+   ")
        actual_graph = ASCIITreeLog.show_tree(self.r0, graph_arrangement="{connection}")
        self.assertEqual(expected_graph, actual_graph)

    def test_multiple_branch(self):
        self.r0.add_downstream(self.n1)
        self.r0.add_downstream(self.n2)
        self.r0.add_downstream(self.b1)
        self.r0.add_downstream(self.b2)
        expected_graph=("|       \n"
                        "+       \n"
                        "├─┬─┬─╮ \n"
                        "| | | + \n"
                        "| | |   \n"
                        "| | +   \n"
                        "| |     \n"
                        "| +     \n"
                        "|       \n"
                        "+       ")
        actual_graph = ASCIITreeLog.show_tree(self.r0, graph_arrangement="{connection}")
        self.assertEqual(expected_graph, actual_graph)

    def test_simple_merge(self):
        self.r0.add_downstream(self.n1)
        self.r0.add_downstream(self.n2)
        self.n1.add_downstream(self.n2)
        expected_graph=("|   \n"
                        "+   \n"
                        "├─╮ \n"
                        "| + \n"
                        "├─╯ \n"
                        "+   ")
        actual_graph = ASCIITreeLog.show_tree(self.r0, graph_arrangement="{connection}")
        self.assertEqual(expected_graph, actual_graph)

    def test_horizon_flow_not_overwrite_vertical_flow(self):
        self.r0.add_downstream(self.n1)
        self.r0.add_downstream(self.n2)
        self.r0.add_downstream(self.b1)
        self.n1.add_downstream(self.b1)
        expected_graph=("|     \n"
                        "+     \n"
                        "├─┬─╮ \n"
                        "| | + \n"
                        "├─|─╯ \n"
                        "| +   \n"
                        "|     \n"
                        "+     ")
        actual_graph = ASCIITreeLog.show_tree(self.r0, graph_arrangement="{connection}")
        self.assertEqual(expected_graph, actual_graph)

if __name__ == '__main__':
    unittest.main()
