import os

from htmlnode import ParentNode
from textnode import text_node_to_html_node
from delimiter import text_to_textnodes
from pathlib import Path

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def extract_title(markdown):
    lines = markdown.split("\n")
    if len(lines) == 0:
        return None
    if not lines[0].startswith("# "):
        return None
    return lines[0][2:]

def markdown_to_blocks(markdown):
    block_strings = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        block_strings.append(block)
    return block_strings

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_olist
    return block_type_paragraph

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return block_to_paragraph_node(block)
    if block_type == block_type_heading:
        return block_to_heading_node(block)
    if block_type == block_type_code:
        return block_to_code_node(block)
    if block_type == block_type_quote:
        return block_to_quote_node(block)
    if block_type == block_type_ulist:
        return block_to_ulist_node(block)
    if block_type == block_type_olist:
        return block_to_olist_node(block)
    raise ValueError("Unknown block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def block_to_paragraph_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children, None)

def block_to_heading_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError("Invalid heading")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def block_to_code_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def block_to_quote_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.strip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def block_to_ulist_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def block_to_olist_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as md_file:
        md_content = md_file.read()
        html_string = markdown_to_html_node(md_content).to_html()
        title = extract_title(md_content)
    with open(template_path) as template_file:
        template_content = template_file.read()
        replace_template_title = template_content.replace("{{ Title }}", title)
        replace_template_content = replace_template_title.replace("{{ Content }}", html_string)
        
    dir_path = os.path.dirname(dest_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(dest_path, "w") as dest_file:
        dest_file.write(replace_template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_path = Path(dir_path_content)
    dest_path = Path(dest_dir_path)

    for entry in os.listdir(dir_path_content):
        source = content_path / entry
        destination = dest_path / entry

        if source.is_file() and source.suffix == '.md':
            html_path = destination.with_suffix('.html')
            html_path.parent.mkdir(parents=True, exist_ok=True)
            generate_page(source, template_path, html_path)
        elif source.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            generate_pages_recursive(source, template_path, destination)
