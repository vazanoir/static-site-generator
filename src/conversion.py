from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode
from nodesplit import (
    split_nodes_link,
    split_nodes_image,
    split_nodes_delimiter,
)
from block import (
    block_to_block_type,
    get_heading_length,
)
from md_types import (
    TextTypes,
    BlockTypes
)


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


def block_to_html(block):
    block_type = block_to_block_type(block)
    block_types = BlockTypes()

    match block_type:
        case block_types.heading:
            heading_length = get_heading_length(block)

            children = []
            for node in text_to_text_nodes(block[heading_length + 1:]):
                children.append(text_node_to_html_node(node))
            return ParentNode(children, f"h{heading_length}")

        case block_types.code:
            return ParentNode([LeafNode(block[3:-3].strip(), "code")], "pre")

        case block_types.quote:
            new_block = ""
            for line in block.split("\n"):
                new_block += line[2:] + "\n"

            children = []
            for node in text_to_text_nodes(new_block.strip()):
                children.append(text_node_to_html_node(node))
            return ParentNode(children, "blockquote")

        case block_types.unordered_list:
            children = []
            for line in block.split("\n"):
                inner_children = []
                for node in text_to_text_nodes(line[2:]):
                    inner_children.append(text_node_to_html_node(node))
                children.append(ParentNode(inner_children, "li"))
            return ParentNode(children, "ul")

        case block_types.ordered_list:
            children = []
            for line in block.split("\n"):
                inner_children = []
                for node in text_to_text_nodes(line[3:]):
                    inner_children.append(text_node_to_html_node(node))
                children.append(ParentNode(inner_children, "li"))
            return ParentNode(children, "ol")

        case _:
            children = []
            for node in text_to_text_nodes(block):
                children.append(text_node_to_html_node(node))

            return ParentNode(children, "p")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    output = []
    for block in blocks:
        output.append(block_to_html(block))

    return ParentNode(output, "div")
