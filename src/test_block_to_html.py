import unittest

from markdown_blocks import extract_title, markdown_to_html_node


class TestTitleExtract(unittest.TestCase):
    def test_extraction(self):
        md = """
# This is the header

blahblahblah
"""
        node = extract_title(md)
        self.assertEqual(node, "This is the header")

    def test_extraction2(self):
        md = """


# This is a working header
"""
        node = extract_title(md)
        self.assertEqual(node, "This is a working header")

    def test_extraction_error(self):
        md = """
### This should raise an error
"""
        self.assertRaises(Exception, extract_title, md)

    def test_extraction_error2(self):
        md = """
#This is another cause for error
"""
        self.assertRaises(Exception, extract_title, md)


class TestBlockToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote(self):
        md = """
> This is a quote by *ME*, **ME!!**

>And another quote
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote> This is a quote by *ME*, <b>ME!!</b></blockquote><blockquote>And another quote</blockquote></div>",
        )


if __name__ == "__main__":
    unittest.main()
