import unittest

from textnode import BlockType,block_to_block_type

class TestTextNodeToHTML(unittest.TestCase):
    def test_block_to_type_heading(self):
        text ="###### This is a header"
        output = block_to_block_type(text)
        self.assertEqual(BlockType.HEADING,output)
    def test_block_to_type_code(self):
        text ="``` code block ```"
        output = block_to_block_type(text)
        self.assertEqual(BlockType.CODE,output)
if __name__ == "__main__":
    unittest.main()