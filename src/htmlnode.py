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
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None or self.value == "":
            raise ValueError()
        if self.tag == None or self.tag == "":
            return value
        return "<" + self.tag + self.props_to_html() + ">" + self.value + "</" + self.tag + ">"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError()
        if self.children == None:
            raise ValueError()
        result = "<" + self.tag + ">"
        for child in self.children:
            result += child.to_html()
        result += "</" + self.tag + ">"
        return result