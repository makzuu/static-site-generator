import unittest
from textnode import TextNode
from inline import (split_nodes_delimiter, extract_markdown_images,
                    extract_markdown_links, split_nodes_image, split_nodes_link,
                    text_to_textnodes, TEXT_TYPE_TEXT, TEXT_TYPE_BOLD, TEXT_TYPE_ITALIC,
                    TEXT_TYPE_CODE, TEXT_TYPE_IMAGE, TEXT_TYPE_LINK)

class TestInline(unittest.TestCase):
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

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
                [
                    TextNode("This is ", TEXT_TYPE_TEXT),
                    TextNode("text", TEXT_TYPE_BOLD),
                    TextNode(" with an ", TEXT_TYPE_TEXT),
                    TextNode("italic", TEXT_TYPE_ITALIC),
                    TextNode(" word and a ", TEXT_TYPE_TEXT),
                    TextNode("code block", TEXT_TYPE_CODE),
                    TextNode(" and an ", TEXT_TYPE_TEXT),
                    TextNode("image", TEXT_TYPE_IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and a ", TEXT_TYPE_TEXT),
                    TextNode("link", TEXT_TYPE_LINK, "https://boot.dev")
                    ], nodes)

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
