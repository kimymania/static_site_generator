import unittest

from htmlnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_span(self):
        node = LeafNode(
            "span",
            "Hello, Python!",
            {
                "class": "hello",
                "id": "intro",
            },
        )
        self.assertEqual(
            node.to_html(), "<span class='hello' id='intro'>Hello, Python!</span>"
        )

    def test_leaf_to_html_raw(self):
        node = LeafNode(None, "Raw String")
        self.assertEqual(node.to_html(), "Raw String")


if __name__ == "__main__":
    unittest.main()
