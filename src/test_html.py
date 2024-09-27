import unittest

from html import (
    text_node_to_html_node,
    TextTypes,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link
)
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

    def test_extract_markdown_images(self):
        text = (
            "This is text with a "
            "![rick roll](https://i.imgur.com/aKaOqIh.gif) and "
            "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and this "
            "[to youtube](https://www.youtube.com/@bootdotdev) a link"
        )
        output = extract_markdown_images(text)
        self.assertEqual(output, [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ])

    def test_extract_markdown_links(self):
        text = (
            "This is text with a link "
            "[to boot dev](https://www.boot.dev) and "
            "[to youtube](https://www.youtube.com/@bootdotdev) and this "
            "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) an image"
        )
        output = extract_markdown_links(text)
        self.assertEqual(output, [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ])

    def test_split_nodes_image(self):
        text_types = TextTypes()
        nodes = [
            TextNode(
                'some really *spicy* and random [link]("https://boot.dev")',
                text_types.text
            ),
            TextNode(
                (
                    'some really *spicy* and random '
                    '![image]("https://boot.dev/img.png")'
                ),
                text_types.text
            ),
            TextNode(
                (
                    'some really *spicy* and random '
                    '![fox]("https://boot.dev/fox.png") and this '
                    '![chicken]("https://boot.dev/chicken.png")'
                ),
                text_types.text
            ),
        ]

        output = split_nodes_image(nodes)
        self.assertEqual(output, [
            TextNode(
                'some really *spicy* and random [link]("https://boot.dev")',
                text_types.text
            ),
            TextNode(
                'some really *spicy* and random ',
                text_types.text
            ),
            TextNode("image", text_types.image, "https://boot.dev/img.png"),
            TextNode(
                'some really *spicy* and random ',
                text_types.text
            ),
            TextNode("fox", text_types.image, "https://boot.dev/fox.png"),
            TextNode(
                ' and this ',
                text_types.text
            ),
            TextNode("chicken", text_types.image, "https://boot.dev/chicken.png"),
        ])

    def test_split_nodes_link(self):
        text_types = TextTypes()
        nodes = [
            TextNode(
                'some really *spicy* and random [link]("https://boot.dev")',
                text_types.text
            ),
            TextNode(
                'some really *spicy* and random '
                '[link]("https://shoe.dev") and '
                '[LINK]("https://shutdown.dev")',
                text_types.text
            ),
            TextNode(
                (
                    'some really *spicy* and random '
                    '![image]("https://boot.dev/img.png")'
                ),
                text_types.text
            ),
        ]

        output = split_nodes_link(nodes)
        self.assertEqual(output, [
            TextNode(
                'some really *spicy* and random ',
                text_types.text
            ),
            TextNode("link", text_types.link, 'https://boot.dev'),
            TextNode(
                'some really *spicy* and random ',
                text_types.text
            ),
            TextNode("link", text_types.link, 'https://shoe.dev'),
            TextNode(" and ", text_types.text),
            TextNode("LINK", text_types.link, 'https://shutdown.dev'),
            TextNode(
                'some really *spicy* and random '
                '![image]("https://boot.dev/img.png")',
                text_types.text
            ),
        ])


if __name__ == "__main__":
    unittest.main()
