import unittest

from html import text_node_to_html_node, TextTypes, split_nodes_delimiter
from textnode import TextNode


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

    def test_split_nodes_delimiter(self):
        text_types = TextTypes()
        nodes = [
            TextNode(
                "some really *spicy* and random `hello world`! **BOLD!**",
                text_types.text
            ),
            TextNode(
                "spicy and random",
                text_types.italic
            ),
            TextNode(
                "some **really** spicy and *random* `hello world`! **BOLD!**",
                text_types.text
            ),
            TextNode(
                "some really *spicy and random* `hello world`! `BOLD!`",
                text_types.text
            ),
            TextNode(
                "spicy and random",
                text_types.bold
            )
        ]

        output = split_nodes_delimiter(nodes, "*", text_types.italic)
        self.assertEqual(output, [
            TextNode("some really ", text_types.text),
            TextNode("spicy", text_types.italic),
            TextNode(" and random `hello world`! **BOLD!**", text_types.text),
            TextNode("spicy and random", text_types.italic),
            TextNode("some **really** spicy and ", text_types.text),
            TextNode("random", text_types.italic),
            TextNode(" `hello world`! **BOLD!**", text_types.text),
            TextNode("some really ", text_types.text),
            TextNode("spicy and random", text_types.italic),
            TextNode(" `hello world`! `BOLD!`", text_types.text),
            TextNode("spicy and random", text_types.bold)
        ])
        output = split_nodes_delimiter(output, "**", text_types.bold)
        self.assertEqual(output, [
            TextNode("some really ", text_types.text),
            TextNode("spicy", text_types.italic),
            TextNode(" and random `hello world`! ", text_types.text),
            TextNode("BOLD!", text_types.bold),
            TextNode("spicy and random", text_types.italic),
            TextNode("some ", text_types.text),
            TextNode("really", text_types.bold),
            TextNode(" spicy and ", text_types.text),
            TextNode("random", text_types.italic),
            TextNode(" `hello world`! ", text_types.text),
            TextNode("BOLD!", text_types.bold),
            TextNode("some really ", text_types.text),
            TextNode("spicy and random", text_types.italic),
            TextNode(" `hello world`! `BOLD!`", text_types.text),
            TextNode("spicy and random", text_types.bold)
        ])
        output = split_nodes_delimiter(output, "`", text_types.code)
        self.assertEqual(output, [
            TextNode("some really ", text_types.text),
            TextNode("spicy", text_types.italic),
            TextNode(" and random ", text_types.text),
            TextNode("hello world", text_types.code),
            TextNode("! ", text_types.text),
            TextNode("BOLD!", text_types.bold),
            TextNode("spicy and random", text_types.italic),
            TextNode("some ", text_types.text),
            TextNode("really", text_types.bold),
            TextNode(" spicy and ", text_types.text),
            TextNode("random", text_types.italic),
            TextNode(" ", text_types.text),
            TextNode("hello world", text_types.code),
            TextNode("! ", text_types.text),
            TextNode("BOLD!", text_types.bold),
            TextNode("some really ", text_types.text),
            TextNode("spicy and random", text_types.italic),
            TextNode(" ", text_types.text),
            TextNode("hello world", text_types.code),
            TextNode("! ", text_types.text),
            TextNode("BOLD!", text_types.code),
            TextNode("spicy and random", text_types.bold)
        ])


if __name__ == "__main__":
    unittest.main()
