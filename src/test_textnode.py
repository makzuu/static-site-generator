import unittest

from textnode import (TextNode, split_nodes_delimiter, split_nodes_image,
                      split_nodes_link, TEXT_TYPE_TEXT, TEXT_TYPE_BOLD,
                      TEXT_TYPE_ITALIC, TEXT_TYPE_CODE, TEXT_TYPE_LINK,
                      TEXT_TYPE_IMAGE)

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

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TEXT_TYPE_CODE)
        expected = [
                TextNode("This is text with a ", TEXT_TYPE_TEXT),
                TextNode("code block", TEXT_TYPE_CODE),
                TextNode(" word", TEXT_TYPE_TEXT),
                ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter2(self):
        node = TextNode("`print(\"Hello, World\")` # imprime 'Hello, World' en la terminal", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TEXT_TYPE_CODE)
        expected = [
                TextNode("print(\"Hello, World\")", TEXT_TYPE_CODE),
                TextNode(" # imprime 'Hello, World' en la terminal", TEXT_TYPE_TEXT),
                ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter3(self):
        node = TextNode("bold text", TEXT_TYPE_BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TEXT_TYPE_BOLD)
        expected = [
                TextNode("bold text", TEXT_TYPE_BOLD)
                ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image(self):
        node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TEXT_TYPE_TEXT,
                )
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes,
                         [
                             TextNode("This is text with an ", TEXT_TYPE_TEXT),
                             TextNode("image", TEXT_TYPE_IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                             TextNode(" and another ", TEXT_TYPE_TEXT),
                             TextNode(
                                 "second image", TEXT_TYPE_IMAGE, "https://i.imgur.com/3elNhQu.png"
                                 ),
                             ]
                         )

    def test_split_nodes_image2(self):
        node = TextNode("", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [])

    def test_split_nodes_image3(self):
        node = TextNode("just text", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            node
            ])

    def test_split_nodes_link(self):
        node = TextNode(
                "This is text with a [link](https://www.boot.dev) and another [second link](https://archlinux.org)",
                TEXT_TYPE_TEXT,
                )
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes,
                         [
                             TextNode("This is text with a ", TEXT_TYPE_TEXT),
                             TextNode("link", TEXT_TYPE_LINK, "https://www.boot.dev"),
                             TextNode(" and another ", TEXT_TYPE_TEXT),
                             TextNode(
                                 "second link", TEXT_TYPE_LINK, "https://archlinux.org"
                                 ),
                             ]
                         )

    def test_split_nodes_link2(self):
        node = TextNode("", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [])

    def test_split_nodes_link3(self):
        node = TextNode("just text", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            node
            ])

if __name__ == "__main__":
    unittest.main()
