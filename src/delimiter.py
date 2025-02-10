import re
from textnode import TextType, TextNode

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes =[]
    inside_delimiter = False
    i = 0
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        current_text = ""
        i = 0
        while i < len(node.text):
            if node.text[i:i+len(delimiter)] == delimiter:
                if inside_delimiter:
                    # Closing delimiter found
                    new_nodes.append(TextNode(current_text, text_type))
                    current_text = ""
                    inside_delimiter = False
                else:
                    # Opening delimiter found
                    if current_text:
                        new_nodes.append(TextNode(current_text, TextType.TEXT))
                    current_text = ""
                    inside_delimiter = True
                i += len(delimiter)  # Skip past the delimiter
            else:
                # Accumulate the current character
                current_text += node.text[i]
                i += 1
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    if inside_delimiter:
        raise ValueError(f"Invalid Markdown: Missing closing delimiter for '{delimiter}'")

    return new_nodes 

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        for image in matches:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        for match in matches:
            sections = original_text.split(f"[{match[0]}]({match[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
splitted = text_to_textnodes(text)