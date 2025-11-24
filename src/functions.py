from nodes import TextNode, HTMLNode, LeafNode, ParentNode
from enums import TextType, BlockType
import re

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", text_node.text, {"src": text_node.url, "alt": text_node.text})

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        strings = node.text.split(delimiter)
        sub = False
        for string in strings:
            if string == "":
                sub = not sub
                continue
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

def markdown_to_blocks(markdown):
    split_string = markdown.split("\n\n")
    result = []
    for string in split_string:
        if string != "":
            result.append(string.strip())
    return result

def block_to_block_type(block):
    if block.startswith("# ") or block.startswith("## ") or block.startswith("### ") or block.startswith("#### ") or block.startswith("##### ") or block.startswith("###### "):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    result = BlockType.PARAGRAPH
    if block.startswith(">"):
        result = BlockType.QUOTE
    if block.startswith("- "):
        result = BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        result = BlockType.ORDERED_LIST
    i = 1
    for line in block.split("\n"):
        if result == BlockType.PARAGRAPH:
            break
        if result == BlockType.QUOTE:
            if line.startswith(">"):
                continue
            else:
                result = BlockType.PARAGRAPH
                break
        if result == BlockType.UNORDERED_LIST:
            if line.startswith("- "):
                continue
            else:
                result = BlockType.PARAGRAPH
                break
        if result == BlockType.ORDERED_LIST:
            if line.startswith(f"{i}. "):
                i += 1
                continue
            else:
                result = BlockType.PARAGRAPH
                break
    return result

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            nodes.append(text_to_parent_node("p", block))
            continue
        if block_type == BlockType.HEADING:
            split_text = block.split(" ", 1)
            nodes.append(text_to_parent_node(f"h{len(split_text[0])}", split_text[1]))
            continue
        if block_type == BlockType.CODE:
            text_only = block[4:-3]
            nodes.append(ParentNode("pre", [LeafNode("code", text_only)]))
            continue
        split_text = block.split("\n")
        if block_type == BlockType.QUOTE:
            nodes.append(text_to_parent_node("blockquote", "\n".join(map(lambda x: x[1:], split_text))))
            continue
        inner_nodes = []
        for line in split_text:
            inner_nodes.append(text_to_parent_node("li", line.split(" ", 1)[1]))
        tag = "ul" if block_type == BlockType.UNORDERED_LIST else "ol"
        nodes.append(ParentNode(tag, inner_nodes))
    return ParentNode("div", nodes)


def text_to_parent_node(tag, text):
    nodes = []
    text_nodes = text_to_textnodes(text.replace("\n", " "))
    for node in text_nodes:
        nodes.append(text_node_to_html_node(node))
    return ParentNode(tag, nodes)

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:]
    raise Exception("No Title Found")