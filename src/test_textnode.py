import unittest
from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a different text node", "bold")

        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")

        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", "bold", "archlinux.org")
        node2 = TextNode("This is a text node", "bold", "boot.dev")

        self.assertNotEqual(node, node2)

    def test_default(self):
        node = TextNode("This is a text node", "bold")
        self.assertIsNone(node.url)

    def test_repr(self):
        node = TextNode("This is a text node", "bold", "archlinux.org")
        self.assertEqual("TextNode(This is a text node, bold, archlinux.org)", repr(node))


if __name__ == "__main__":
    unittest.main()
