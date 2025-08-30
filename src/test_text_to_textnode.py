import unittest

from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType


class TestTextToTextNode(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.maxDiff = None

    def test_text1(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_start_with_link(self):
        nodes = text_to_textnodes(
            "[Naver](https://www.naver.com) is the **most **favoured web portal in **KOREA**."
        )
        self.assertEqual(
            nodes,
            [
                TextNode("Naver", TextType.LINK, "https://www.naver.com"),
                TextNode(" is the ", TextType.PLAIN),
                TextNode("most ", TextType.BOLD),
                TextNode("favoured web portal in ", TextType.PLAIN),
                TextNode("KOREA", TextType.BOLD),
                TextNode(".", TextType.PLAIN),
            ],
        )

    def test_continuous_special_nodes(self):
        nodes = text_to_textnodes(
            "`HELLO WORLD`**!!** How is _everyone_ doing? ![smiley](emojis/smiley.png)**^-^**"
        )
        self.assertEqual(
            nodes,
            [
                TextNode("HELLO WORLD", TextType.CODE),
                TextNode("!!", TextType.BOLD),
                TextNode(" How is ", TextType.PLAIN),
                TextNode("everyone", TextType.ITALIC),
                TextNode(" doing? ", TextType.PLAIN),
                TextNode("smiley", TextType.IMAGE, "emojis/smiley.png"),
                TextNode("^-^", TextType.BOLD),
            ],
        )

    def test_multiple_links_and_images(self):
        nodes = text_to_textnodes(
            "Check out these links: [GitHub](https://github.com) and [Google](https://google.com) "
            + "And these images: ![cat](cat.jpg) and ![dog](dog.png)"
        )
        self.assertEqual(
            nodes,
            [
                TextNode("Check out these links: ", TextType.PLAIN),
                TextNode("GitHub", TextType.LINK, "https://github.com"),
                TextNode(" and ", TextType.PLAIN),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" And these images: ", TextType.PLAIN),
                TextNode("cat", TextType.IMAGE, "cat.jpg"),
                TextNode(" and ", TextType.PLAIN),
                TextNode("dog", TextType.IMAGE, "dog.png"),
            ],
        )

    def test_special_chars(self):
        nodes = text_to_textnodes(
            "Here's some `code` and **bold** and ![img with * chars](star*.png)"
        )
        self.assertEqual(
            nodes,
            [
                TextNode("Here's some ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode(" and ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("img with * chars", TextType.IMAGE, "star*.png"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
