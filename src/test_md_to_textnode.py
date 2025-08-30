import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from textnode import TextNode, TextType


class TestMarkdownImageExtraction2(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_with_path(self):
        node = TextNode(
            "Check this image: ![local image](/path/to/image.jpg)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Check this image: ", TextType.PLAIN),
                TextNode("local image", TextType.IMAGE, "/path/to/image.jpg"),
            ],
            new_nodes,
        )

    def test_split_image_with_params(self):
        node = TextNode(
            "Image with parameters: ![profile](https://example.com/img.png?size=large&format=jpeg)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image with parameters: ", TextType.PLAIN),
                TextNode(
                    "profile",
                    TextType.IMAGE,
                    "https://example.com/img.png?size=large&format=jpeg",
                ),
            ],
            new_nodes,
        )

    def test_split_image_no_images(self):
        node = TextNode(
            "This is plain text with [a link](https://example.com) but no images",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [node],
            new_nodes,
        )

    def test_split_image_at_boundaries(self):
        node = TextNode(
            "![start image](start.jpg)Middle text![end image](end.jpg)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start image", TextType.IMAGE, "start.jpg"),
                TextNode("Middle text", TextType.PLAIN),
                TextNode("end image", TextType.IMAGE, "end.jpg"),
            ],
            new_nodes,
        )


class TestMarkdownLinkExtraction2(unittest.TestCase):
    def test_split_basic_link(self):
        node = TextNode(
            "This is a [link](https://example.com) in text",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" in text", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_multiple_links(self):
        node = TextNode(
            "Here are [two](https://example.com) and [three](https://another.com) links",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Here are ", TextType.PLAIN),
                TextNode("two", TextType.LINK, "https://example.com"),
                TextNode(" and ", TextType.PLAIN),
                TextNode("three", TextType.LINK, "https://another.com"),
                TextNode(" links", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_link_with_params(self):
        node = TextNode(
            "Complex link: [click here](https://api.example.com/data?id=123&type=user)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Complex link: ", TextType.PLAIN),
                TextNode(
                    "click here",
                    TextType.LINK,
                    "https://api.example.com/data?id=123&type=user",
                ),
            ],
            new_nodes,
        )

    def test_split_link_no_links(self):
        node = TextNode(
            "This is plain text with an ![image](https://example.com/img.jpg) but no links",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [node],
            new_nodes,
        )

    def test_split_link_at_boundaries(self):
        node = TextNode(
            "[start](https://start.com)Middle text[end](https://end.com)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.LINK, "https://start.com"),
                TextNode("Middle text", TextType.PLAIN),
                TextNode("end", TextType.LINK, "https://end.com"),
            ],
            new_nodes,
        )


class TestMarkdownLinkExtraction(unittest.TestCase):
    def test_extract_simple_link(self):
        text = "Here is a [link](https://www.example.com) in text"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("link", "https://www.example.com")])

    def test_extract_multiple_links(self):
        text = "Here are [two](http://example.com) [links](http://another.com) in text"
        links = extract_markdown_links(text)
        self.assertEqual(
            links, [("two", "http://example.com"), ("links", "http://another.com")]
        )

    def test_extract_link_with_path(self):
        text = "Check out our [docs](/documentation/guide) for more info"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("docs", "/documentation/guide")])

    def test_extract_link_with_parameters(self):
        text = "Click [here](https://api.example.com/data?id=123&type=user)"
        links = extract_markdown_links(text)
        self.assertEqual(
            links, [("here", "https://api.example.com/data?id=123&type=user")]
        )

    def test_no_links_in_text(self):
        text = "This is plain text with no links, but has ![image](pic.jpg)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [])


class TestMarkdownImageExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_simple_image(self):
        text = "This is ![alt](https://example.com/image.png) an image."
        images = extract_markdown_images(text)
        self.assertEqual(images, [("alt", "https://example.com/image.png")])

    def test_extract_multiple_images(self):
        text = "Here are ![img1](url1.png) and ![img2](url2.png) images"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("img1", "url1.png"), ("img2", "url2.png")])

    def test_extract_image_with_path(self):
        text = "Complex URL ![image](/path/to/image/file.jpg)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("image", "/path/to/image/file.jpg")])

    def test_extract_image_with_full_url(self):
        text = (
            "Image with full URL ![pic](https://website.com/images/pic.png?size=large)"
        )
        images = extract_markdown_images(text)
        self.assertEqual(
            images, [("pic", "https://website.com/images/pic.png?size=large")]
        )

    def test_no_image_in_text(self):
        text = "This is just [a link](https://example.com) and plain text"
        images = extract_markdown_images(text)
        self.assertEqual(images, [])


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
