from enum import Enum
from leafnode import LeafNode
import re
class TextType(Enum):
	TEXT = "text"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"

class TextNode():
	def __init__(self,text,text_type,url=None):
		self.text = text
		self.text_type = text_type
		self.url = url
	
	def __eq__(self, other):
		return self.text == other.text and self.text_type == other.text_type and self.url == other.url
		
	
	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
	match (text_node.text_type):
		case TextType.TEXT:
			return LeafNode(None,text_node.text)
		case TextType.BOLD:
			return LeafNode("b",text_node.text)
		case TextType.ITALIC:
			return LeafNode("i",text_node.text)
		case TextType.CODE:
			return LeafNode("code",text_node.text)
		case TextType.LINK:
			return LeafNode("a",text_node.text,{"href" : text_node.url})
		case TextType.IMAGE:
			return LeafNode("code","",{"src" : text_node.url , "alt" : text_node.text})
		case _:
			raise Exception("Incorrect TextType")
		
def split_nodes_delimiter(old_nodes,delimiter,text_type):
	node_storage = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			node_storage.append(node)
			continue
		first = node.text.find(delimiter)
		second = node.text.find(delimiter,first+1)
		if first == -1 or second == -1:
			node_storage.append(node)
			continue
			#raise Exception("Can't find delimiter pair") 
		before = node.text[:first]
		middle = node.text[first + len(delimiter):second]
		after= node.text[second + len(delimiter):]
		if before:
			node_storage.append(TextNode(before,TextType.TEXT))
			
		node_storage.append(TextNode(middle,text_type))
		if after:
			node_storage.append(TextNode(after, TextType.TEXT))

	return node_storage

def split_nodes_image(old_nodes):
	node_storage = []
	for node in old_nodes:
		if images := extract_markdown_images(node.text):
			for alt_text,url in images:
				new_text = node.text.split(f"![{alt_text}]({url})",1)
				if new_text[0]:
					node_storage.append(TextNode(new_text[0],TextType.TEXT))
				node_storage.append(TextNode(alt_text,TextType.IMAGE,url))
				node.text = new_text[1]
			if node.text:
				node_storage.append(TextNode(node.text,TextType.TEXT))

		else:
			node_storage.append(node)
			continue 
	
	return node_storage


def split_nodes_link(old_nodes):
	node_storage = []
	for node in old_nodes:
		if images := extract_markdown_links(node.text):
			for alt_text,url in images:
				new_text = node.text.split(f"[{alt_text}]({url})",1)
				if new_text[0]:
					node_storage.append(TextNode(new_text[0],TextType.TEXT))
				node_storage.append(TextNode(alt_text,TextType.LINK,url))
				node.text = new_text[1]
			if node.text:
				node_storage.append(TextNode(node.text,TextType.TEXT))
		else:
			node_storage.append(node)
			continue 
	return node_storage


def extract_markdown_images(text):
	result = []
	matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
	result.extend(matches)
	return result

def extract_markdown_links(text):
	result = []
	matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
	result.extend(matches)
	return result

def text_to_textnodes(text):
	nodes = [TextNode(text,TextType.TEXT)]
	nodes = split_nodes_delimiter(nodes,"**",TextType.BOLD)
	nodes = split_nodes_delimiter(nodes,"*",TextType.ITALIC)
	nodes = split_nodes_delimiter(nodes,"`",TextType.CODE)

	nodes = split_nodes_image(nodes)
	nodes = split_nodes_link(nodes)
	return nodes

def markdown_to_blocks(markdown):
	lines = markdown.split("\n")
	blocks = []
	output = ""
	for i in range(0,len(lines)):
		if lines[i] == "":
			blocks.append(output)
			output = ""
		else:
			output += lines[i].strip()
			if i == len(lines)-1:
				blocks.append(output)
				continue
			if lines[i+1] != "":
				output += "\n" 
			
	return blocks
