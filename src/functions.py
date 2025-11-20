from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
import re

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
        strings = node.text.split(delimiter)
        sub = False
        for string in strings:
            if sub:
                result.append(TextNode(string, text_type))
                sub = False
            else:
                result.append(TextNode(string, node.text_type))
                sub = True
        if not sub:
            raise Exception("closing delimeter missing")
    return result

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if images == [] or node.text_type != TextType.TEXT:
            result.append(node)
            continue
        text = node.text
        for image in images:
            split_text = text.split(f"![{image[0]}]({image[1]})", 1)
            if split_text[0] != "":
                result.append(TextNode(split_text[0], TextType.TEXT))
            result.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text = split_text[1]
        if text != "":
            result.append(TextNode(text, TextType.TEXT))
    return result

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if links == [] or node.text_type != TextType.TEXT:
            result.append(node)
            continue
        text = node.text
        for link in links:
            split_text = text.split(f"[{link[0]}]({link[1]})", 1)
            if split_text[0] != "":
                result.append(TextNode(split_text[0], TextType.TEXT))
            result.append(TextNode(link[0], TextType.LINK, link[1]))
            text = split_text[1]
        if text != "":
            result.append(TextNode(text, TextType.TEXT))
    return result

def text_to_textnodes(text):
    original_nodes = [TextNode(text, TextType.TEXT)]
    with_bold = split_nodes_delimiter(original_nodes, "**", TextType.BOLD)
    with_italic = split_nodes_delimiter(with_bold, "_", TextType.ITALIC)
    with_code = split_nodes_delimiter(with_italic, "`", TextType.CODE)
    with_images = split_nodes_image(with_code)
    with_links = split_nodes_link(with_images)
    return with_links

