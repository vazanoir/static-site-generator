import unittest

from block import markdown_to_blocks, BlockTypes, block_to_block_type


class TestBlock(unittest.TestCase):
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

    def test_block_to_block_type(self):
        # Heading
        block_type = block_to_block_type("## Test")
        self.assertEqual(block_type, BlockTypes().heading)

        # Paragraph
        block_type = block_to_block_type("Test")
        self.assertEqual(block_type, BlockTypes().paragraph)

        # OL
        block_type = block_to_block_type("1. Test")
        self.assertEqual(block_type, BlockTypes().ordered_list)

        block_type = block_to_block_type("1. Test\n2. test\n3. test")
        self.assertEqual(block_type, BlockTypes().ordered_list)

        block_type = block_to_block_type("1. Test\n3. Wrong")
        self.assertNotEqual(block_type, BlockTypes().ordered_list)

        # UL
        block_type = block_to_block_type("- Test")
        self.assertEqual(block_type, BlockTypes().unordered_list)

        block_type = block_to_block_type("- Test\n- test\n- test")
        self.assertEqual(block_type, BlockTypes().unordered_list)

        block_type = block_to_block_type("- Test\n - test\n- test")
        self.assertNotEqual(block_type, BlockTypes().unordered_list)

        block_type = block_to_block_type("- Test\n-test\n- test")
        self.assertNotEqual(block_type, BlockTypes().unordered_list)

        block_type = block_to_block_type("- Test\ntest\n- test")
        self.assertNotEqual(block_type, BlockTypes().unordered_list)

        # Quote
        block_type = block_to_block_type("> Test")
        self.assertEqual(block_type, BlockTypes().quote)

        block_type = block_to_block_type("> Test\n> Test\n> test")
        self.assertEqual(block_type, BlockTypes().quote)

        block_type = block_to_block_type("> Test\n>Test\n> test")
        self.assertNotEqual(block_type, BlockTypes().quote)

        block_type = block_to_block_type("> Test\n > Test\n> test")
        self.assertNotEqual(block_type, BlockTypes().quote)

        block_type = block_to_block_type("> Test\nTest\n> test")
        self.assertNotEqual(block_type, BlockTypes().quote)

        # Code
        block_type = block_to_block_type("```Test```")
        self.assertEqual(block_type, BlockTypes().code)

        block_type = block_to_block_type(
            "``` sh\necho -e 'bonjour'\nsleep 1```"
        )
        self.assertEqual(block_type, BlockTypes().code)
