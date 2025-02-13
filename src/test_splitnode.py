import unittest

from textnode import TextNode, split_nodes_delimiter, TextType, markdown_to_blocks

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

    def test_markdown_to_block(self):
        markdown ="""# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(3,len(blocks))
if __name__ == "__main__":
    unittest.main()