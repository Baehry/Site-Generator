class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        result = ""
        if self.props == None:
            return ""
        for prop in props:
            result += " " + prop + "=\"" + props[prop] + "\""
        return result
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, value, tag, props=None):
        super().__init__(value, tag, None, props)
    def to_html(self):
        if self.value == None or self.value == "":
            raise ValueError()
        if self.tag == None:
            return value
        return "<" + self.tag + self.props_to_html() + ">" + self.value + "</" + self.tag + ">"