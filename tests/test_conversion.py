import unittest

from conversion import (
    text_node_to_html_node,
    text_to_text_nodes,
    markdown_to_blocks,
    markdown_to_html_node,
)
from textnode import TextNode
from md_types import TextTypes


class TestHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = (
                "# This is a heading\n\n"
                "This is a paragraph of text. "
                "It has some **bold** and *italic* words inside of it.\n\n"
                "* This is the first list item in a list block\n"
                "* This is a list item\n"
                "* This is another list item"
        )

        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "# This is a heading",
            (
                "This is a paragraph of text. "
                "It has some **bold** and *italic* words inside of it."
            ),
            (
                "* This is the first list item in a list block\n"
                "* This is a list item\n"
                "* This is another list item"
            )
        ])

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

    def test_markdown_to_html_node(self):
        output = markdown_to_html_node("""![Photos de crêpes](https://crepes.com/image.jpg)

# Recette de la pâte à crêpes

Tiré de la *fameuse recette* disponible sur [Internet](https://crepes.com/recette)

## Ingrédients

* Des œufs
* De la farine
* Du lait
* Du sucre
* ~~De l'huile de coude~~

> N'hésitez pas à faire **moitié-moitié** avec du sucre vanillé pour plus de goût !

## Étapes

1. Mettre la farine
2. Ajouter les œufs, le sucre, l'huile et le beurre
3. Mélanger délicatement
4. Faire cuire les crêpes une par une dans une poêle légère

## Partager

Pour intégrer cette recette sur votre site web, vous pouvez copier-coller le code suivante :

```html
<iframe href="https://crepes.com/recette?embed"></iframe>
```""")


if __name__ == "__main__":
    unittest.main()
