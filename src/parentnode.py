from htmlnode import HTMLNode

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError
        if self.children == None:
            raise ValueError
        else:
            children_html = ""
            for node in self.children:
                children_html += node.to_html()
            return f"<{self.tag}>{children_html}</{self.tag}>"