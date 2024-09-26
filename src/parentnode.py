from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, children, tag=None, props=None):
        super().__init__(children=children, tag=tag, props=props)

    def __repr__(self):
        return f"ParentNode ({self.tag}, {self.children}, {self.props})"

    def to_html(self):
        if self.tag is None:
            raise ValueError("parent node need a tag")

        if self.children is None or len(self.children) <= 0:
            raise ValueError("parent node without children")

        html = f"<{self.tag}>"
        for child in self.children:
            if isinstance(child, HTMLNode):
                html += child.to_html()
        html += f"</{self.tag}>"
        return html
