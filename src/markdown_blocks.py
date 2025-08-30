import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"


def block_to_block_type(block: str):
    prefix = re.findall(r"^(#{1,6}|```|>|-|\d+\.)", block)
    if not prefix:
        return BlockType.PARAGRAPH
    elif prefix[0].startswith("#"):
        return BlockType.HEADING
    elif prefix[0] == "```" and len(re.findall(r"```$", block)) == 1:
        return BlockType.CODE
    elif prefix[0] == ">":
        return BlockType.QUOTE
    elif prefix[0] == "-":
        return BlockType.UNORDERED_LIST
    elif "." in prefix[0]:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    """Input: raw markdown, Output: list of 'block' strings"""
    blocks: list[str] = markdown.split("\n\n")
    final = []
    for block in blocks:
        temp = block.strip()
        if temp:
            final.append(temp)

    return final


def markdown_to_html_node(markdown):
    """Convert full markdown document into a single parent HTMLNode
    Nested elements should become child HTMLNode objects"""
    pass
