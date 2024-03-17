from htmlnode import HTMLNode
from htmlnode import LeafNode
import unittest


class TestHTMLNode(unittest.TestCase):
    def test_tag_is_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)

    def test_value_is_none(self):
        node = HTMLNode()
        self.assertIsNone(node.value)

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.boot.dev", "class": "link"})
        expected = " href=\"https://www.boot.dev\" class=\"link\""
        self.assertEqual(node.props_to_html(), expected)

    def test_repr(self):
        node = HTMLNode(tag="a", value="boot.dev", props={"href": "https://www.boot.dev"})
        expected = "HTMLNode(a, boot.dev, None, {'href': 'https://www.boot.dev'})"
        self.assertEqual(repr(node), expected)


class TeastLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        expected = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = "<a href=\"https://www.google.com\">Click me!</a>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html3(self):
        node = LeafNode()
        self.assertRaises(ValueError, node.to_html)

    def test_to_html4(self):
        node = LeafNode(value="This is a paragraph of text.")
        expected = "This is a paragraph of text."
        self.assertEqual(node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
