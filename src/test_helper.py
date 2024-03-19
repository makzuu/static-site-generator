import unittest
from helper import extract_markdown_images, extract_markdown_links

class Helper(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png"), ("another", "https://i.imgur.com/dfsdkjfd.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images2(self):
        text = ""
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        expected = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links2(self):
        text = ""
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

if __name__ == "__main__":
    unittest.main()
