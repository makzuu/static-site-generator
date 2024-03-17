from htmlnode import LeafNode

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
