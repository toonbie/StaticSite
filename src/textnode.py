from enum import Enum
from leafnode import LeafNode
from parentnode import ParentNode
from leafnode import LeafNode
import re
class TextType(Enum):
	TEXT = "text"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED = "unordered_list"
	ORDERED = "ordered_list"


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

def block_to_block_type(block):
	lines = block.split("\n")
	if re.match(r"#{1,6} \w+",lines[0]):
			return BlockType.HEADING
	if re.match(r"^```",lines[0]) and re.match(r"^```$",lines[-1]) or re.match(r"^```.*?```$",lines[0]):
			return BlockType.CODE
	is_quote = True
	is_unordered = True
	is_ordered = True
	for i in range(0,len(lines)):
		if not any([is_quote,is_unordered,is_ordered]):
			break
		if not re.match(r"^>",lines[i]):
			is_quote = False
		if not re.match(r"^(\*|-) ",lines[i]):
			is_unordered = False
		if not re.match(rf"^{i+1}. ",lines[i]):
			is_ordered = False
	if is_quote:
		return BlockType.QUOTE
	elif is_unordered:
		return BlockType.UNORDERED
	elif is_ordered:
		return BlockType.ORDERED
	else:
		return BlockType.PARAGRAPH
	
def markdown_to_html_node(markdown):
	htmlnodes = []
	blocks = markdown_to_blocks(markdown)
	for block in blocks:
		block_type = block_to_block_type(block)
		match(block_type):
			case BlockType.PARAGRAPH:
				children = text_to_children(block)
				paragraph = ParentNode("p",children)
				htmlnodes.append(paragraph)
			case BlockType.HEADING:
				hashtagSeperated = re.match(r"^(#+) ",block).group()
				headingSize = hashtagSeperated.count("#")
				if headingSize > 6:
					headingSize = 6
				text = re.sub(r"^(#+) ", "", block)
				children = text_to_children(text)
				tag = f"h{headingSize}"
				heading = ParentNode(tag,children)
				htmlnodes.append(heading)
			case BlockType.QUOTE:
				text = re.sub(r"^> ","",block, flags=re.M)
				children = text_to_children(text)
				quote = ParentNode("blockquote", children)
				htmlnodes.append(quote)
			case BlockType.CODE:
				text = re.sub(r"^```|```$","",block, flags=re.M)
				children = ParentNode("code",[LeafNode(None,text)])
				code = ParentNode("pre", children)
				htmlnodes.append(code)
			case BlockType.UNORDERED:
				text = re.sub(r"^(\*|-) ","",block, flags=re.M)
				lines = text.split("\n")
				li_nodes = []
				for line in lines:
					children = text_to_children(line)
					li_nodes.append(ParentNode("li",children))
				ul_node = ParentNode("ul", li_nodes)
				htmlnodes.append(ul_node)
			case BlockType.ORDERED:
				text = re.sub(r"^\d. ","",block, flags=re.M)
				lines = text.split("\n")
				li_nodes = []
				for line in lines:
					children = text_to_children(line)
					li_nodes.append(ParentNode("li",children))
				ol_node = ParentNode("ol", li_nodes)
				htmlnodes.append(ol_node)
	return ParentNode("div",htmlnodes)

def text_to_children(text):
	text_nodes = text_to_textnodes(text)
	children = []
	for text_node in text_nodes:
		match text_node.text_type:
			case TextType.TEXT:
				children.append(LeafNode(None,text_node.text))
			case TextType.BOLD:
				text_child = LeafNode(None,text_node.text)
				children.append(ParentNode("strong",[text_child]))
			case TextType.ITALIC:
				text_child = LeafNode(None,text_node.text)
				children.append(ParentNode("em",[text_child]))
			case TextType.CODE:
				text_child = LeafNode(None,text_node.text)
				children.append(ParentNode("code",[text_child]))	
	return children