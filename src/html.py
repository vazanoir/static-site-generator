from leafnode import LeafNode
from textnode import TextNode
import re


class TextTypes():
    def __init__(self):
        self.text = "text"
        self.bold = "bold"
        self.italic = "italic"
        self.code = "code"
        self.link = "link"
        self.image = "image"

    def is_valid_type(self, type_to_test):
        return type_to_test in self.__dict__


def text_node_to_html_node(text_node):
    text_types = TextTypes()

    if not text_types.is_valid_type(text_node.text_type):
        raise Exception("invalid text type")

    match text_node.text_type:
        case text_types.text:
            return LeafNode(text_node.text)
        case text_types.bold:
            return LeafNode(text_node.text, tag="b")
        case text_types.italic:
            return LeafNode(text_node.text, tag="i")
        case text_types.code:
            return LeafNode(text_node.text, tag="code")
        case text_types.link:
            return LeafNode(text_node.text, tag="a", props={
                "href": text_node.url
            })
        case text_types.image:
            return LeafNode("", tag="img", props={
                "src": text_node.url,
                "alt": text_node.text
            })


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    text_types = TextTypes()
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_types.text:
            new_nodes.append(old_node)
            continue

        splitted_text = []
        if text_type == text_types.italic:
            safe_split = old_node.text.replace("**", "@@").split(delimiter)
            splitted_text = list(map(
                lambda text: text.replace("@@", "**"),
                safe_split
            ))
        else:
            splitted_text = old_node.text.split(delimiter)

        for text in splitted_text:
            i = splitted_text.index(text)

            if text == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(text, text_types.text))
            else:
                new_nodes.append(TextNode(text, text_type))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.+?)\]\((.+?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"[^!]\[(.+?)\]\((.+?)\)", text)
