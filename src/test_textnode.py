import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("Google", "link", "www.google.com")
        node2 = TextNode("Google", "link", "www.google.co.kr")
        self.assertNotEqual(node, node2)

    def test_text_diff(self):
        node = TextNode("Identical", "italic")
        node2 = TextNode("Identical", "bold")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
