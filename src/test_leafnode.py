import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
	def test_to_html_error(self):
		node= LeafNode(None,None)
		with self.assertRaises(ValueError):
			node.to_html()

	def test_to_html_no_props(self):
		node= LeafNode("p", "This is a paragraph of text.")
		self.assertEqual(node.to_html(),"<p>This is a paragraph of text.</p>")

	def test__to_html_with_props(self):
		node= LeafNode("a", "Click me!", {"href": "https://www.google.com"})
		self.assertEqual(node.to_html(),"<a href=\"https://www.google.com\">Click me!</a>")

if __name__ == "__main__":
    unittest.main()