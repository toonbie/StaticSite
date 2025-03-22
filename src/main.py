from textnode import  TextNode
from textnode import TextType
from PageFuncs import empty_then_copy

def main():
	node1 =TextNode("This is a text node",TextType.BOLD,"https://www.boot.dev")	
	print(node1.__repr__())
	empty_then_copy()
main()
