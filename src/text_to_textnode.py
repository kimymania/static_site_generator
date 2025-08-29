from md_to_textnode import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


def text_to_textnodes(text: str):
    final = []
    final = split_nodes_delimiter([TextNode(text, TextType.PLAIN)], "**", TextType.BOLD)
    final = split_nodes_delimiter(final, "_", TextType.ITALIC)
    final = split_nodes_delimiter(final, "`", TextType.CODE)
    final = split_nodes_image(final)
    final = split_nodes_link(final)

    return final
