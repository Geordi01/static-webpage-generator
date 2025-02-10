import re
from textnode import TextType, TextNode

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.NORMAL:
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
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(image[0], TextType.IMAGES, image[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.NORMAL:
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
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(match[0], TextType.LINKS, match[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL))

    return new_nodes

node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.NORMAL,
)
new_nodes = split_nodes_link([node])
