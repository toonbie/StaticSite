import unittest

from textnode import BlockType,block_to_block_type,markdown_to_html_node

class TestTextNodeToHTML(unittest.TestCase):
    def test_block_to_type_heading(self):
        text ="###### This is a header"
        output = block_to_block_type(text)
        self.assertEqual(BlockType.HEADING,output)
        
    def test_block_to_type_code(self):
        text ="``` code block ```"
        output = block_to_block_type(text)
        self.assertEqual(BlockType.CODE,output)

    def test_paragraph_to_html(self):
        text = "This is a paragraph"
        expected = "<div><p>This is a paragraph</p></div>"
        self.assertEqual(markdown_to_html_node(text).to_html(), expected)
    
    def test_heading_to_html(self):
        text = "# This is a heading"
        expected = "<div><h1>This is a heading</h1></div>"
        self.assertEqual(markdown_to_html_node(text).to_html(), expected)
    
    def test_unordered_list_to_html(self):
        text = "* Item 1\n* Item 2"
        expected = "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>"
        self.assertEqual(markdown_to_html_node(text).to_html(), expected)
    
    def test_multiple_blocks_to_html(self):
        text = "# Header\n\nParagraph text\n\n* List item"
        expected = "<div><h1>Header</h1><p>Paragraph text</p><ul><li>List item</li></ul></div>"
        self.assertEqual(markdown_to_html_node(text).to_html(), expected)
        

if __name__ == "__main__":
    unittest.main()