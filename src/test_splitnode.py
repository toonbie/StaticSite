import unittest

from textnode import TextNode, split_nodes_delimiter, TextType

class TestSplitNode(unittest.TestCase):
    def test_split_success(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,
[
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
])
        
    def test_split_success_non_text(self):
        node = TextNode("This is text with a `code block` word", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a `code block` word", TextType.CODE)])

if __name__ == "__main__":
    unittest.main()