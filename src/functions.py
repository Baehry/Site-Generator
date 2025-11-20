from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.Bold:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextNode.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextNode.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        strings = node.text.split(delimeter)
        sub = False
        for string in strings:
            if sub:
                result.append(string, text_type)
                sub = True
            else:
                result.append(string, node.text_type)
                sub = False
        if not sub:
            raise Exception("closing delimeter missing")
    return result