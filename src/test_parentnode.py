import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
	def test_to_html_parent(self):
		node = ParentNode("div", [
            LeafNode("b", "Bold"),
            LeafNode(None, "Normal"),
            LeafNode("i", "Italic")
        ])
		self.assertEqual(node.to_html(),"<div><b>Bold</b>Normal<i>Italic</i></div>")

	def test_to_html_parent_with_parents(self):
		parent = ParentNode("div", [
            ParentNode("p", [
                LeafNode("b", "Bold text"),
                LeafNode("i", "Italic text")
            ]),
            LeafNode("span", "Normal text")
        ])
		self.assertEqual(parent.to_html(),"<div><p><b>Bold text</b><i>Italic text</i></p><span>Normal text</span></div>")

	def test__to_html_errors_no_tag(self):
		node = ParentNode(None, [LeafNode("b", "Bold")])
		with self.assertRaises(ValueError):
			node.to_html()


	def test__to_html_errors_no_children(self):
		node = ParentNode("div", None)
		with self.assertRaises(ValueError):
			node.to_html()

if __name__ == "__main__":
    unittest.main()