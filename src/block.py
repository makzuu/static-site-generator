from htmlnode import HTMLNode, ParentNode, LeafNode
from inline import text_to_textnodes, text_node_to_html_node

BLOCK_TYPE_PARAGRAPH = "paragraph"
BLOCK_TYPE_HEADING = "heading"
BLOCK_TYPE_CODE = "code"
BLOCK_TYPE_QUOTE = "quote"
BLOCK_TYPE_UNORDERED_LIST = "unordered_list"
BLOCK_TYPE_ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    return list(
            map(
                lambda line: line.strip(),
                filter(
                    lambda line: len(line) != 0,
                    markdown.split("\n\n")
                    )
                )
            )

def get_start(lines):
    start = lines[0].split(" ")[0]
    filter_function = lambda current: current == start
    if start[:-1].isdigit() and start[-1] == ".":
        filter_function = lambda current: current[:-1].isdigit() and current[-1] == "."
    filtered_lines = filter(
            filter_function,
            map(
                lambda line: line.split(" ")[0],
                lines
                )
            )
    if len(list(filtered_lines)) != len(lines):
        return None
    return start

def block_to_block_type(block):
    heading = block.split(" ")[0]
    if heading.endswith("#") and len(heading) < 7:
        return BLOCK_TYPE_HEADING
    if block.startswith("```") and block.endswith("```"):
        return BLOCK_TYPE_CODE
    lines = block.split("\n")
    start = get_start(lines)
    if start == ">":
        return BLOCK_TYPE_QUOTE
    if start == "*" or start == "-":
        return BLOCK_TYPE_UNORDERED_LIST
    if start != None and start[:-1].isdigit() and start[-1] == ".":
        return BLOCK_TYPE_ORDERED_LIST
    return BLOCK_TYPE_PARAGRAPH

def paragraph_block_to_htmlnode(block):
    text = " ".join(block.split("\n"))
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return ParentNode("p", html_nodes)

def heading_block_to_htmlnode(block):
    sections = block.split(" ")
    text = " ".join(sections[1:])
    heading_lv = sections[0].count("#")

    html_nodes = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return ParentNode(f"h{heading_lv}", html_nodes)

def code_block_to_htmlnode(block):
    value = block[4:len(block) - 4]
    return ParentNode("pre", [ParentNode("code", [LeafNode(None, value)])])

def quote_block_to_htmlnode(block):
    lines = block.split("\n")
    text = " ".join(map(lambda line: line.strip("> "), lines))
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return ParentNode("blockquote", html_nodes)

def unordered_list_block_to_htmlnode(block):
    lines = block.split("\n")
    li_children = []
    children = []
    for line in lines:
        text_nodes = text_to_textnodes(line[2:])
        for text_node in text_nodes:
            li_children.append(text_node_to_html_node(text_node))
        children.append(ParentNode("li", li_children))
        li_children = []
    return ParentNode("ul", children)

def ordered_list_block_to_htmlnode(block):
    lines = block.split("\n")
    li_children = []
    children = []
    for line in lines:
        line = " ".join(line.split()[1:])
        text_nodes = text_to_textnodes(line)
        for text_node in text_nodes:
            li_children.append(text_node_to_html_node(text_node))
        children.append(ParentNode("li", li_children))
        li_children = []
    return ParentNode("ol", children)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        if type is BLOCK_TYPE_PARAGRAPH:
            nodes.append(paragraph_block_to_htmlnode(block))
        if type is BLOCK_TYPE_HEADING:
            nodes.append(heading_block_to_htmlnode(block))
        if type is BLOCK_TYPE_CODE:
            nodes.append(code_block_to_htmlnode(block))
        if type is BLOCK_TYPE_QUOTE:
            nodes.append(quote_block_to_htmlnode(block))
        if type is BLOCK_TYPE_UNORDERED_LIST:
            nodes.append(unordered_list_block_to_htmlnode(block))
        if type is BLOCK_TYPE_ORDERED_LIST:
            nodes.append(ordered_list_block_to_htmlnode(block))
    return ParentNode("div", nodes)
