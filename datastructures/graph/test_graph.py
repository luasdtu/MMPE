'''
Created on 23/01/2014

@author: MMPE
'''
import unittest
from datastructures.graph.graph import UndirectedGraph, Tree


class TestGraph(unittest.TestCase):

    def setUp(self):
        self.g = UndirectedGraph()
        for a, b, c in [('Mads', 'Ellen', ('dad', 'child')), ('Mads', 'Agnes', 'parent-child'), ('Mads', 'Per', ('son', 'dad')), ('Per', 'Marie', ('dad', 'daughter')), ('Per', 'Magnus', 'parent-child'), ('Sine', 'Mads', 'Wife'), ('Hans', 'Inger', 'Wife')]:
            self.g.add_edge(a, b, c)

    def test_add_edge(self):
        self.assertTrue('Ellen' in  self.g.edges['Mads'])


    def test_add_edge_relation(self):

        self.assertTrue('Ellen' in  self.g.edges['Mads'])
        self.assertEqual(self.g.relations['Mads']['Ellen'], 'child')
        self.assertEqual(self.g.relations['Ellen']['Mads'], 'dad')
        self.assertEqual(self.g.tree('Mads').to_str(), """Mads
- Sine(Wife)
- Ellen(child)
- Per(dad)
- - Marie(daughter)
- - Magnus(parent-child)
- Agnes(parent-child)
""")

    def test_tree2str(self):
        g = UndirectedGraph()
        for a, b, c in [('Mads', 'Ellen', ('dad', 'child')), ('Mads', 'Agnes', 'parent-child'), ('Mads', 'Per', ('son', 'dad')), ('Per', 'Marie', ('dad', 'daughter')), ('Per', 'Magnus', 'parent-child'), ('Sine', 'Mads', 'Wife'), ('Hans', 'Inger', 'Wife')]:
            g.add_edge(a, b)
        self.assertEqual(g.tree('Mads').to_str(), """Mads
- Sine
- Ellen
- Per
- - Marie
- - Magnus
- Agnes
""")


    def test_tree_list(self):
        self.assertEqual(self.g.tree('Mads').to_lst(), [('Mads', 'Sine', 'Wife'), ('Mads', 'Ellen', 'child'), ('Mads', 'Per', 'dad'), ('Per', 'Marie', 'daughter'), ('Per', 'Magnus', 'parent-child'), ('Mads', 'Agnes', 'parent-child')])


    def test_tree_list2(self):
        g = UndirectedGraph()
        for a, b, c in [('Mads', 'Ellen', ('dad', 'child')), ('Mads', 'Agnes', 'parent-child'), ('Mads', 'Per', ('son', 'dad')), ('Per', 'Marie', ('dad', 'daughter')), ('Per', 'Magnus', 'parent-child'), ('Sine', 'Mads', 'Wife'), ('Hans', 'Inger', 'Wife')]:
            g.add_edge(a, b)
        self.assertEqual(g.tree('Mads').to_lst(), [('Mads', 'Sine', None), ('Mads', 'Ellen', None), ('Mads', 'Per', None), ('Per', 'Marie', None), ('Per', 'Magnus', None), ('Mads', 'Agnes', None)])


    def test_forest_to_str(self):
        self.assertEqual(self.g.forest(['Mads', 'Hans']).to_str(), """Mads
- Sine(Wife)
- Ellen(child)
- Per(dad)
- - Marie(daughter)
- - Magnus(parent-child)
- Agnes(parent-child)
Hans
- Inger(Wife)
""")

    def test_forest_to_lst(self):
        self.assertEqual(self.g.forest(['Mads', 'Hans']).to_lst(), [('Mads', 'Sine', 'Wife'), ('Mads', 'Ellen', 'child'), ('Mads', 'Per', 'dad'), ('Per', 'Marie', 'daughter'), ('Per', 'Magnus', 'parent-child'), ('Mads', 'Agnes', 'parent-child'), ('Hans', 'Inger', 'Wife')])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_add_edge']
    unittest.main()
