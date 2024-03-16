from htmlnode import HTMLNode
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


if __name__ == "__main__":
    unittest.main()
