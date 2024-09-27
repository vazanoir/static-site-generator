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


def split_nodes_image(old_nodes):
    text_types = TextTypes()
    new_nodes = []

    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)

        if len(images) < 1:
            new_nodes.append(old_node)
            continue

        previous = ""
        for image in images:
            before, after = old_node.text.split(
                f"![{image[0]}]({image[1]})",
                1
            )

            new_nodes.append(
                TextNode(before.replace(previous, ""), text_types.text)
            )
            new_nodes.append(TextNode(image[0], text_types.image, image[1]))

            if image == images[len(images) - 1] and after != "":
                new_nodes.append(TextNode(after, text_types.text))

            previous = before + f"![{image[0]}]({image[1]})"

    return new_nodes


def split_nodes_link(old_nodes):
    text_types = TextTypes()
    new_nodes = []

    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)

        if len(links) < 1:
            new_nodes.append(old_node)
            continue

        previous = ""
        for link in links:
            before, after = old_node.text.split(f"[{link[0]}]({link[1]})", 1)

            new_nodes.append(
                TextNode(before.replace(previous, ""), text_types.text)
            )
            new_nodes.append(TextNode(link[0], text_types.link, link[1]))

            if link == links[len(links) - 1] and after != "":
                new_nodes.append(TextNode(after, text_types.text))

            previous = before + f"[{link[0]}]({link[1]})"

    return new_nodes


def text_to_text_nodes(text):
    text_types = TextTypes()
    nodes = [TextNode(text, text_types.text)]
    nodes = split_nodes_delimiter(nodes, "**", text_types.bold)
    nodes = split_nodes_delimiter(nodes, "*", text_types.italic)
    nodes = split_nodes_delimiter(nodes, "`", text_types.code)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes


def markdown_to_blocks(text):
    blocks = text.split("\n\n")
    return list(map(lambda block: block.strip(), blocks))
