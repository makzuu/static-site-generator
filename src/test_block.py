import unittest
from block import markdown_to_blocks

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

if __name__ == "__main__":
    unittest.main()
