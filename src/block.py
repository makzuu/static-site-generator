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
