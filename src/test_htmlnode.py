import unittest

from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Unknown text type")


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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("p", "First paragraph")
        child2 = LeafNode("p", "Second paragraph")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent.to_html(),
            "<div><p>First paragraph</p><p>Second paragraph</p></div>",
        )

    def test_to_html_nested_with_props(self):
        inner = LeafNode("span", "text", {"class": "highlight"})
        outer = ParentNode("div", [inner], {"id": "container"})
        self.assertEqual(
            outer.to_html(),
            "<div><span class='highlight'>text</span></div>",
        )

    def test_to_html_empty_props(self):
        node = LeafNode("p", "text", {})
        self.assertEqual(node.to_html(), "<p>text</p>")

    def test_to_html_with_special_characters(self):
        node = LeafNode("p", "Hello & goodbye < > !")
        self.assertEqual(node.to_html(), "<p>Hello & goodbye < > !</p>")

    def test_to_html_complex_nested_structure(self):
        leaf1 = LeafNode("b", "Bold text")
        leaf2 = LeafNode("i", "Italic text")
        inner_parent = ParentNode("p", [leaf1, leaf2])
        leaf3 = LeafNode("span", "Normal text", {"class": "text"})
        outer_parent = ParentNode("div", [inner_parent, leaf3])
        self.assertEqual(
            outer_parent.to_html(),
            "<div><p><b>Bold text</b><i>Italic text</i></p><span class='text'>Normal text</span></div>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("Bold Text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>Bold Text</b>")

    def test_text_node_to_html_node_code(self):
        text_node = TextNode("print('Hello')", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<code>print('Hello')</code>")

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("Click me", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            html_node.to_html(), "<a href='https://example.com'>Click me</a>"
        )

    def test_text_node_to_html_node_image(self):
        text_node = TextNode(
            "Image description", TextType.IMAGE, "https://example.com/image.jpg"
        )
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            html_node.to_html(),
            "<img src='https://example.com/image.jpg' alt='Image description'>",
        )

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("Italic Text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<i>Italic Text</i>")


if __name__ == "__main__":
    unittest.main()
