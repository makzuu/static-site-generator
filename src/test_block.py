import unittest
from block import (markdown_to_blocks, block_to_block_type,
BLOCK_TYPE_PARAGRAPH, BLOCK_TYPE_HEADING, BLOCK_TYPE_CODE, BLOCK_TYPE_QUOTE,
BLOCK_TYPE_UNORDERED_LIST, BLOCK_TYPE_ORDERED_LIST)

class TestBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        self.assertEqual(markdown_to_blocks(markdown),
                         [
                             "This is **bolded** paragraph",
                             "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                             "* This is a list\n* with items"
                             ])

    def test_markdown_to_blocks2(self):
        markdown = ""
        self.assertEqual(markdown_to_blocks(markdown), [])

    def test_markdown_to_blocks3(self):
        markdown = "\n## Heading     "
        self.assertEqual(markdown_to_blocks(markdown), ["## Heading"])

    def test_block_to_block_type(self):
        block = "# Title"
        self.assertEqual(block_to_block_type(block), BLOCK_TYPE_HEADING)

    def test_block_to_block_type2(self):
        block = "#Title"
        self.assertEqual(block_to_block_type(block), BLOCK_TYPE_PARAGRAPH)

    def test_block_to_block_type3(self):
        block = "###### Titulo 2"
        self.assertEqual(block_to_block_type(block), BLOCK_TYPE_HEADING)

    def test_block_to_block_type4(self):
        block = "####### Titulo 2"
        self.assertEqual(block_to_block_type(block), BLOCK_TYPE_PARAGRAPH)

    def test_block_to_block_type5(self):
        block = "```print(\"Hello World\")\nsome_function()```"
        self.assertEqual(block_to_block_type(block), BLOCK_TYPE_CODE)

    def test_block_to_block_type6(self):
        block = "> some quote\n> another quote"
        self.assertEqual(block_to_block_type(block), BLOCK_TYPE_QUOTE)

    def test_block_to_block_type7(self):
        block = "> some quote\n* another quote"
        self.assertEqual(block_to_block_type(block), BLOCK_TYPE_PARAGRAPH)

    def test_block_to_block_type8(self):
        block = "* comprar pan\n* comprar bebida"
        self.assertEqual(block_to_block_type(block), BLOCK_TYPE_UNORDERED_LIST)

    def test_block_to_block_type9(self):
        block = "- comprar pan\n- comprar bebida"
        self.assertEqual(block_to_block_type(block), BLOCK_TYPE_UNORDERED_LIST)

    def test_block_to_block_type10(self):
        block = "1. list item\n2. another list item"
        self.assertEqual(block_to_block_type(block), BLOCK_TYPE_ORDERED_LIST)


if __name__ == "__main__":
    unittest.main()
