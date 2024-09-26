from textnode import TextNode
from leafnode import LeafNode


def main():
    node = TextNode("this is an image of a fox", "image", "https://boot.dev/fox-image.png")
    leaf = text_node_to_html_node(node)
    print(leaf.to_html())


def text_node_to_html_node(text_node):
    text_types = ("text", "bold", "italic", "code", "link", "image")

    if text_types[0] == text_node.text_type:
        return LeafNode(text_node.text)
    elif text_types[1] == text_node.text_type:
        return LeafNode(text_node.text, tag="b")
    elif text_types[2] == text_node.text_type:
        return LeafNode(text_node.text, tag="i")
    elif text_types[3] == text_node.text_type:
        return LeafNode(text_node.text, tag="code")
    elif text_types[4] == text_node.text_type:
        return LeafNode(text_node.text, tag="a", props={"href": text_node.url})
    elif text_types[5] == text_node.text_type:
        return LeafNode("", tag="img", props={
            "src": text_node.url,
            "alt": text_node.text}
        )
    else:
        raise Exception("invalid text type")


if __name__ == "__main__":
    main()
