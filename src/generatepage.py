from block import markdown_to_html_node
import os

def extract_title(markdown):
    lines = markdown.split("\n")
    title_list = list(filter(lambda line: line.startswith("# "), lines))
    if len(title_list) != 1:
        raise Exception("Markdown Syntax Error: No title found")
    return title_list[0][2:]

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    directory_name = os.path.dirname(dest_path)
    if directory_name != "":
        os.makedirs(directory_name, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template.replace("{{ Title }}", title).replace("{{ Content }}", html))

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for file in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(file_path):
            generate_page(file_path, template_path, dest_path.replace("md", "html"))
        else:
            generate_pages_recursive(file_path, template_path, dest_path)
