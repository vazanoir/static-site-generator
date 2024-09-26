from textnode import TextNode
from html import text_node_to_html_node


def main():
    node = TextNode("this is an image of a fox", "image", "https://boot.dev/fox-image.png")
    leaf = text_node_to_html_node(node)
    print(leaf.to_html())


if __name__ == "__main__":
    main()
