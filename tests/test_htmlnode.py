import unittest

from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_default(self):
        node = HTMLNode()

        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props_to_html(self):
        node = HTMLNode(
            tag="a",
            props={"href": "https://boot.dev", "alt": "cool stuff"}
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://boot.dev" alt="cool stuff"'
        )

        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_to_html(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)


if __name__ == "__main__":
    unittest.main()
