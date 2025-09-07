import os
import re
from enum import Enum

from htmlnode import LeafNode, ParentNode, text_node_to_html_node
from inline_markdown import text_to_textnodes


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


def markdown_to_blocks(markdown: str) -> list[str]:
    """Input: raw markdown, Output: list of 'block' strings"""
    blocks: list[str] = markdown.split(os.linesep + os.linesep)
    final = []
    for block in blocks:
        temp = block.strip()
        if temp:
            final.append(temp)

    return final


def markdown_to_html_node(markdown: str) -> ParentNode:
    """Convert full markdown document into a single parent HTMLNode
    Nested elements should become child HTMLNode objects"""
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        blocktype = block_to_block_type(block)
        if blocktype == BlockType.CODE:
            child = LeafNode("code", filter_codeblock(block))
            children.append(ParentNode("pre", [child]))
        elif blocktype == BlockType.PARAGRAPH:
            child = text_to_html_node(filter_paragraph(block))
            children.append(ParentNode("p", child))
        elif blocktype == BlockType.HEADING:
            child = text_to_html_node(block.replace("#", "").strip())
            header = re.findall(r"^(#{1,6})", markdown)
            if len(header[0]) == 1:
                children.append(ParentNode("h1", child))
            elif len(header[0]) == 2:
                children.append(ParentNode("h2", child))
            elif len(header[0]) == 3:
                children.append(ParentNode("h3", child))
            elif len(header[0]) == 4:
                children.append(ParentNode("h4", child))
            elif len(header[0]) == 5:
                children.append(ParentNode("h5", child))
            elif len(header[0]) == 6:
                children.append(ParentNode("h6", child))
        elif blocktype == BlockType.QUOTE:
            lines = block.split("\n")
            list_nodes = []
            for line in lines:
                prefix = re.findall(r"^>", line)
                # Add linebreak to respect newlines
                if line != lines[-1]:
                    line = line + "<br>"
                list_nodes.extend(text_to_html_node(line.lstrip(prefix[0]).lstrip()))
            children.append(ParentNode("blockquote", list_nodes))
        elif blocktype == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            list_nodes = []
            for line in lines:
                prefix = re.findall(r"^(\d+\.\s?)", line)
                child = text_to_html_node(line.lstrip(prefix[0]))
                list_nodes.append(ParentNode("li", child))
            children.append(ParentNode("ol", list_nodes))
        elif blocktype == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            list_nodes = []
            for line in lines:
                prefix = re.findall(r"^(-\s?)", line)
                child = text_to_html_node(line.lstrip(prefix[0]))
                list_nodes.append(ParentNode("li", child))
            children.append(ParentNode("ul", list_nodes))

    result = ParentNode("div", children)
    return result


def text_to_html_node(text: str) -> list[LeafNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))

    return html_nodes


def filter_paragraph(text: str) -> str:
    return text.replace("\n", " ")


def filter_codeblock(text: str) -> str:
    return text.strip("```").lstrip("\n")


def extract_title(markdown):
    """Pulls h1 header from markdown file"""
    header = re.findall(r"^#{1}\s(.*)", markdown.lstrip())
    if not header:
        raise Exception("No h1 title found")
    return header[0].strip()
