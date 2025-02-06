import unittest

from textnode import TextNode, TextType ,text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_None_Url(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, "www.tesco.co.uk")
        self.assertNotEqual(node, node2)

    def test_not_eq_textType(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.CODE, "www.tesco.co.uk")
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_node_TEXT(self):
        nodeText = TextNode("This is a text node", TextType.TEXT, None)
        htmlText = text_node_to_html_node(nodeText)
        self.assertEqual(htmlText.to_html(),"This is a text node")
    
    def test_text_node_to_html_node_LINK(self):
        nodeLink = TextNode("This is a text node", TextType.LINK, "www.tesco.co.uk")
        htmlLink = text_node_to_html_node(nodeLink)
        self.assertEqual(htmlLink.to_html(),"<a href=\"www.tesco.co.uk\">This is a text node</a>")

if __name__ == "__main__":
    unittest.main()
