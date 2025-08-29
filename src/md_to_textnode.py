import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        temp_node = []
        new_strings = node.text.split(delimiter)

        if len(new_strings) % 2 == 0:
            raise Exception("Delimiter was not closed")

        plain = True
        for string in new_strings:
            if string == "":
                plain = False
                continue
            if plain:
                temp_node.append(TextNode(string, node.text_type))
                plain = False
            else:
                temp_node.append(TextNode(string, text_type))
                plain = True
        new_nodes.extend(temp_node)

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        temp_node = []
        text = node.text
        matches: list = extract_markdown_images(text)

        if not matches:
            new_nodes.append(node)
            continue

        split_text = []
        for match in matches:
            split_text = text.split(f"![{match[0]}]({match[1]})", 1)
            if split_text[0] != "":
                temp_node.append(TextNode(split_text[0], node.text_type))
            temp_node.append(TextNode(match[0], TextType.IMAGE, match[1]))
            text = split_text[1]
        else:
            if split_text[1] != "":
                temp_node.append(TextNode(split_text[1], node.text_type))
        new_nodes.extend(temp_node)

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        temp_node = []
        text = node.text
        matches: list = extract_markdown_links(text)

        if not matches:
            new_nodes.append(node)
            continue

        split_text = []
        for match in matches:
            split_text = text.split(f"[{match[0]}]({match[1]})", 1)
            if split_text[0] != "":
                temp_node.append(TextNode(split_text[0], node.text_type))
            temp_node.append(TextNode(match[0], TextType.LINK, match[1]))
            text = split_text[1]
        else:
            if split_text[1] != "":
                temp_node.append(TextNode(split_text[1], node.text_type))
        new_nodes.extend(temp_node)

    return new_nodes


def extract_markdown_images(text):
    # ![alt_text](link_to_image)
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    # [text](url_link)
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches
