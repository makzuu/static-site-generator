from textnode import TextNode
from htmlnode import LeafNode
import re

TEXT_TYPE_TEXT = "text"
TEXT_TYPE_BOLD = "bold"
TEXT_TYPE_ITALIC = "italic"
TEXT_TYPE_CODE = "code"
TEXT_TYPE_LINK = "link"
TEXT_TYPE_IMAGE = "image"

def text_node_to_html_node(text_node):
    if text_node.text_type == "text":
        return LeafNode(None, text_node.text)
    if text_node.text_type == "bold":
        return LeafNode("b", text_node.text)
    if text_node.text_type == "italic":
        return LeafNode("i", text_node.text)
    if text_node.text_type == "code":
        return LeafNode("code", text_node.text)
    if text_node.text_type == "link":
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == "image":
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError("Invalid text_type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TEXT_TYPE_TEXT:
            new_nodes.append(node)
            continue
        items = node.text.split(delimiter)
        if len(items) % 2 == 0:
            raise Exception(f"Invalid markdown syntax: close delimiter ({delimiter}) not found")
        for i in range(0, len(items)):
            if i % 2 == 0:
                if len(items[i]) == 0:
                    continue
                new_nodes.append(TextNode(items[i], TEXT_TYPE_TEXT, None))
            else:
                new_nodes.append(TextNode(items[i], text_type, None))
    return new_nodes

# and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        images = extract_markdown_images(node.text)
        if len(images) == 0 and len(node.text) > 0:
            new_nodes.append(node)
        for image_tup in images:
            splited_text = text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
            if len(splited_text[0]) > 0:
                new_nodes.append(TextNode(splited_text[0], TEXT_TYPE_TEXT))
            text = splited_text[1]
            new_nodes.append(TextNode(image_tup[0], TEXT_TYPE_IMAGE, image_tup[1]))
        if text != "" and text != node.text:
            new_nodes.append(TextNode(text, TEXT_TYPE_TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        links = extract_markdown_links(node.text)
        if len(links) == 0 and len(node.text) > 0:
            new_nodes.append(node)
        for link_tup in links:
            splited_text = text.split(f"[{link_tup[0]}]({link_tup[1]})", 1)
            if len(splited_text[0]) > 0:
                new_nodes.append(TextNode(splited_text[0], TEXT_TYPE_TEXT))
            if len(splited_text) > 1:
                text = splited_text[1]
            else:
                text = ""
            new_nodes.append(TextNode(link_tup[0], TEXT_TYPE_LINK, link_tup[1]))
        if text != "" and text != node.text:
            new_nodes.append(TextNode(text, TEXT_TYPE_TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TEXT_TYPE_TEXT)]
    delimiters = [("**", TEXT_TYPE_BOLD), ("*", TEXT_TYPE_ITALIC), ("`", TEXT_TYPE_CODE)]
    for delimiter in delimiters:
        new_nodes = split_nodes_delimiter(nodes, delimiter[0], delimiter[1])
        nodes = new_nodes
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches
