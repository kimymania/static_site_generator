import unittest

from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_block(self):
        block = "### This is heading 3"
        blocktype = block_to_block_type(block)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_code_block(self):
        block = "``` This is a code block ```"
        blocktype = block_to_block_type(block)
        self.assertEqual(blocktype, BlockType.CODE)

    def test_not_code_block(self):
        block = "``` This is not a code block"
        blocktype = block_to_block_type(block)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_quote_block(self):
        block = "> This is a quote block"
        blocktype = block_to_block_type(block)
        self.assertEqual(blocktype, BlockType.QUOTE)

    def test_unordered_list_block(self):
        block = "-This is an unordered list block"
        blocktype = block_to_block_type(block)
        self.assertEqual(blocktype, BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        block = "1. This is an ordered list block"
        blocktype = block_to_block_type(block)
        self.assertEqual(blocktype, BlockType.ORDERED_LIST)

    def test_normal_paragraph(self):
        block = "This is just a normal paragraph"
        blocktype = block_to_block_type(block)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
