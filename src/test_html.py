import unittest

from html import text_node_to_html_node
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


if __name__ == "__main__":
    unittest.main()
