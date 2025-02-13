import unittest

from textnode import TextNode,TextType,text_to_textnodes

class TestTextNodeToHTML(unittest.TestCase):
    def test_text_node_to_html(self):
        text ="This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(10,len(nodes))

if __name__ == "__main__":
    unittest.main()