import unittest

from src.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_default(self):
        node = LeafNode(None)

        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.props, None)

        self.assertRaises(TypeError, lambda: LeafNode())

    def test_to_html(self):
        node = LeafNode(
            "click here",
            tag="a",
            props={"href": "https://boot.dev", "alt": "cool stuff"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://boot.dev" alt="cool stuff">click here</a>'
        )

        self.assertEqual(LeafNode("").props_to_html(), "")

        self.assertRaises(ValueError, lambda: LeafNode(None).to_html())


if __name__ == "__main__":
    unittest.main()
