import unittest

from conversion import (
    text_node_to_html_node,
    text_to_text_nodes,
)
from textnode import TextNode, TextTypes


class TestHTML(unittest.TestCase):
    def test_text_node_to_html_node(self):
        node = TextNode("some text", "invalid text type")
        self.assertRaises(Exception, lambda: text_node_to_html_node(node))

        node = TextNode("some text", "text")
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.to_html(), "some text")

        node = TextNode("some text", "bold")
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.to_html(), "<b>some text</b>")

        node = TextNode("some text", "link", "https://boot.dev")
        leaf = text_node_to_html_node(node)
        self.assertEqual(
            leaf.to_html(),
            '<a href="https://boot.dev">some text</a>'
        )

        node = TextNode(
            "image of a fox",
            "image",
            "https://boot.dev/fox-image.jpg"
        )
        leaf = text_node_to_html_node(node)
        self.assertEqual(
            leaf.to_html(),
            (
                '<img src="https://boot.dev/fox-image.jpg" '
                'alt="image of a fox"></img>'
            )
        )

    def test_text_to_text_nodes(self):
        text_types = TextTypes()

        text = (
            "This is **text** with an *italic* word and a "
            "`code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )

        output = text_to_text_nodes(text)
        self.assertEqual(output, [
            TextNode("This is ", text_types.text),
            TextNode("text", text_types.bold),
            TextNode(" with an ", text_types.text),
            TextNode("italic", text_types.italic),
            TextNode(" word and a ", text_types.text),
            TextNode("code block", text_types.code),
            TextNode(" and an ", text_types.text),
            TextNode(
                "obi wan image",
                text_types.image,
                "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", text_types.text),
            TextNode("link", text_types.link, "https://boot.dev"),
        ])


if __name__ == "__main__":
    unittest.main()
