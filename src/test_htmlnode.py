import unittest

from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
	def test_props_to_html(self):
		node= HTMLNode(props={"href": "https://www.google.com","target": "_blank",})
		self.assertEqual(node.props_to_html(),"href=\"https://www.google.com\" target=\"_blank\" ")

	def test_props_to_html_None(self):
		node= HTMLNode()
		self.assertEqual(node.props_to_html(),"")

	def test__repr__(self):
		node= HTMLNode()
		self.assertEqual(node.__repr__(),"HTMLNode : tag=None,value=None,children=None,props=None")

if __name__ == "__main__":
    unittest.main()
