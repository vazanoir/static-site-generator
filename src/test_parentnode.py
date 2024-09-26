import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_default(self):
        node = ParentNode(None)

        self.assertEqual(node.tag, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

        self.assertRaises(TypeError, lambda: ParentNode())

    def test_to_html(self):
        node = ParentNode(
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertRaises(ValueError, node.to_html)

        self.assertRaises(ValueError, ParentNode(None).to_html)
        self.assertRaises(ValueError, ParentNode([]).to_html)

        node = ParentNode(
            [
                LeafNode("Bold text", tag="b"),
                LeafNode("Normal text", tag=None),
                LeafNode("italic text", tag="i"),
                LeafNode("Normal text", tag=None),
            ],
            tag="p",
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

        node = ParentNode(
            [
                LeafNode("Bold text", tag="b"),
                LeafNode("Normal text", tag=None),
                LeafNode("italic text", tag="i"),
                ParentNode([
                        LeafNode("Bold text", tag="b"),
                        LeafNode("Normal text", tag=None),
                        LeafNode("italic text", tag="i"),
                    ],
                    tag="span"
                ),
            ],
            tag="p",
        )
        self.assertEqual(
            node.to_html(),
            (
                "<p>"
                "<b>Bold text</b>Normal text<i>italic text</i>"
                "<span><b>Bold text</b>Normal text<i>italic text</i></span>"
                "</p>"
            )
        )


if __name__ == "__main__":
    unittest.main()
