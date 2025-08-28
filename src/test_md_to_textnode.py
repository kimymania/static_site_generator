import unittest

from md_to_textnode import split_nodes_delimiter
from textnode import TextNode, TextType


class TestMarkdownConversion(unittest.TestCase):
    def test_mdconv1(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.PLAIN),
            ],
        )

    def test_bold_text_conversion(self):
        node = TextNode("This is **bold** text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.PLAIN),
            ],
        )

    def test_multiple_code_blocks(self):
        node = TextNode("Here is `code1` and `code2`", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Here is ", TextType.PLAIN),
                TextNode("code1", TextType.CODE),
                TextNode(" and ", TextType.PLAIN),
                TextNode("code2", TextType.CODE),
            ],
        )

    def test_nested_formatting(self):
        node = TextNode("This is **bold** and this is `code`.", TextType.PLAIN)
        bold_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        final_node = []
        for n in bold_nodes:
            if "`" in n.text:
                code_split = split_nodes_delimiter([n], "`", TextType.CODE)
                final_node.extend(code_split)
            else:
                final_node.append(n)
        self.assertEqual(
            final_node,
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" and this is ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode(".", TextType.PLAIN),
            ],
        )

    def test_mixed_formatting_chain(self):
        node = TextNode("_italic_ and `code` mixed", TextType.PLAIN)
        italic_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        final_nodes = []
        for n in italic_nodes:
            if "`" in n.text:
                code_split = split_nodes_delimiter([n], "`", TextType.CODE)
                final_nodes.extend(code_split)
            else:
                final_nodes.append(n)
        self.assertEqual(
            final_nodes,
            [
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode(" mixed", TextType.PLAIN),
            ],
        )

    def test_delimiter_not_closed(self):
        node = TextNode("This `code is not closed", TextType.PLAIN)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(context.exception), "Delimiter was not closed")


if __name__ == "__main__":
    unittest.main()
