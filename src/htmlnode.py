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
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
