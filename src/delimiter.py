from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes =[]
    current_text = ""
    inside_delimiter = False
    i = 0
    for node in old_nodes:
        if node.text_type is not TextType.NORMAL:
            new_nodes.append(node)
            continue
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
                        new_nodes.append(TextNode(current_text, TextType.NORMAL))
                    current_text = ""
                    inside_delimiter = True
                i += len(delimiter)  # Skip past the delimiter
            else:
                # Accumulate the current character
                current_text += node.text[i]
                i += 1

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.NORMAL))
    
    if inside_delimiter:
        raise ValueError(f"Invalid Markdown: Missing closing delimiter for '{delimiter}'")

    return new_nodes 
