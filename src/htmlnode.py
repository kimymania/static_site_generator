class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        # Child classes will override this method
        raise NotImplementedError()

    def props_to_html(self):
        html_string = ""
        if not self.props:
            return html_string

        for k, v in self.props.items():
            html_string += f" {k}='{v}'"
        return html_string

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None) -> None:
        super().__init__(tag, value)
        self.props = props

    def to_html(self):
        if not self.value and not self.tag == "img":
            raise ValueError("LeafNode must have a value")
        if not self.tag:
            return self.value

        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}>{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, props)
        self.children = children

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode requires a tag")
        if not self.children:
            raise ValueError("ParentNode requires children nodes")

        value = ""
        for child in self.children:
            value += child.to_html()

        return f"<{self.tag}>{value}</{self.tag}>"
