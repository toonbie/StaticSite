import functools

class HTMLNode():

    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplemented
    
    def props_to_html(self):
        prop_print = ""
        if self.props == "" or self.props == None:
            return prop_print
        for x,y in self.props.items():
            prop_print += f"{x}=\"{y}\" "
        return prop_print
    
    def __repr__(self):
        return f"HTMLNode : tag={self.tag},value={self.value},children={self.children},props={self.props}"




	
	