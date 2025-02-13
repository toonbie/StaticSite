import unittest

from textnode import TextNode,TextType,split_nodes_link

class TestSplitNodeLink(unittest.TestCase):
    def test_split_empty(self):
        node =  TextNode("",TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes),1)

    def test_split_nodes_one_link(self):
        node = TextNode("This is a [link](https://boot.dev) test", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 3)  

    def test_split_nodes_multi_link(self):
        node = TextNode("Here's [link1](url1) and [link2](url2)", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 4)

if __name__ == "__main__":
    unittest.main()