from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    text: str = old_nodes[0].text

    new_strings = text.split(delimiter)

    if len(new_strings) % 2 == 0:
        raise Exception("Delimiter was not closed")

    plain = True
    for string in new_strings:
        if string == "":
            plain = False
            continue
        if plain:
            new_nodes.append(TextNode(string, TextType.PLAIN))
            plain = False
        else:
            new_nodes.append(TextNode(string, text_type))
            plain = True

    return new_nodes
