from htmlnode import LeafNode
from helper import extract_markdown_images, extract_markdown_links

TEXT_TYPE_TEXT = "text"
TEXT_TYPE_BOLD = "bold"
TEXT_TYPE_ITALIC = "italic"
TEXT_TYPE_CODE = "code"
TEXT_TYPE_LINK = "link"
TEXT_TYPE_IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text != other.text:
            return False

        if self.text_type != other.text_type:
            return False

        if self.url != other.url:
            return False

        return True

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    if text_type == "text":
        return LeafNode(None, text_node.text)
    if text_type == "bold":
        return LeafNode("b", text_node.text)
    if text_type == "italic":
        return LeafNode("i", text_node.text)
    if text_type == "code":
        return LeafNode("code", text_node.text)
    if text_type == "link":
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_type == "image":
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError("Invalid text_type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TEXT_TYPE_TEXT:
            new_nodes.append(node)
            continue
        items = node.text.split(delimiter)
        if len(items) <= 2:
            raise Exception(f"Invalid markdown syntax: close delimiter ({delimiter}) not found")
        for i in range(0, len(items)):
            if i % 2 == 0:
                if len(items[i]) == 0:
                    continue
                new_nodes.append(TextNode(items[i], TEXT_TYPE_TEXT, None))
            else:
                new_nodes.append(TextNode(items[i], text_type, None))
    return new_nodes

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
            if len(splited_text) > 1:
                text = splited_text[1]
            else:
                text = ""
            new_nodes.append(TextNode(image_tup[0], TEXT_TYPE_IMAGE, image_tup[1]))
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
    return new_nodes
