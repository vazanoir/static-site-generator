from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextTypes
from nodesplit import (
    split_nodes_link,
    split_nodes_image,
    split_nodes_delimiter,
)
import block as b


def markdown_to_blocks(text):
    blocks = text.split("\n\n")
    return list(map(lambda block: block.strip(), blocks))


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


def text_to_text_nodes(text):
    text_types = TextTypes()
    nodes = [TextNode(text, text_types.text)]
    nodes = split_nodes_delimiter(nodes, "**", text_types.bold)
    nodes = split_nodes_delimiter(nodes, "*", text_types.italic)
    nodes = split_nodes_delimiter(nodes, "`", text_types.code)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    output = []
    for block in blocks:
        output.append(b.BlockTypes().to_html(block))

    return ParentNode(output, "div")
