from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(value=value, tag=tag, props=props)

    def __repr__(self):
        return f"LeafNode ({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if self.value is None:
            raise ValueError("leaf node must have a value")

        if self.tag is None:
            return str(self.value)

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
