import unittest
from block import *
from htmlnode import HTMLNode

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

    def test_paragraph_block_to_htmlnode(self):
        block = "**this** is a *paragraph*"
        node = paragraph_block_to_htmlnode(block)
        children = [
                LeafNode("b", "this"),
                LeafNode(None, " is a "),
                LeafNode("i", "paragraph")
                ]
        self.assertEqual(node, ParentNode("p", children))

        block = "this is a [link](https://www.boot.dev)\nand this is an image ![image](./img/image1.png)"
        expected = ParentNode("p", [
            LeafNode(None, "this is a "),
            LeafNode("a", "link", {"href": "https://boot.dev"}),
            LeafNode(None, " and this is an image "),
            LeafNode("img", "", {"src": "./img/image1.png", "alt": "image"})
            ])

    def test_heading_block_to_htmlnode(self):
        block = "# this is a heading"
        node = heading_block_to_htmlnode(block)
        self.assertEqual(node, ParentNode("h1", [LeafNode(None, "this is a heading")]))
        block = "### **this** is *another* heading"
        node = heading_block_to_htmlnode(block)
        self.assertEqual(node, ParentNode("h3", [
            LeafNode("b", "this"),
            LeafNode(None, " is "),
            LeafNode("i", "another"),
            LeafNode(None, " heading")
            ]))

    def test_code_block_to_htmlnode(self):
        block = "```\nprint(\"Hello World\")\nsome_function()\n```"
        node = code_block_to_htmlnode(block)
        expected = ParentNode("pre", [
            ParentNode("code", [
                LeafNode(None, "print(\"Hello World\")\nsome_function()")
                ])
            ])
        self.assertEqual(node, expected)

    def test_quote_block_to_htmlnode(self):
        block = "> **some** quote\n> another quote"
        node = quote_block_to_htmlnode(block)
        expected = ParentNode("blockquote", [
            LeafNode("b", "some"),
            LeafNode(None, " quote another quote"),
            ])
        self.assertEqual(node, expected)

    def test_unordered_list_block_to_htmlnode(self):
        block = "- **buy** milk\n- buy cereal"
        node = unordered_list_block_to_htmlnode(block)
        expected = ParentNode("ul", [
            ParentNode("li", [LeafNode("b", "buy"), LeafNode(None, " milk")]),
            ParentNode("li", [LeafNode(None, "buy cereal")])
            ])
        self.assertEqual(node, expected)
        block = "* buy milk\n* buy *cereal*"
        node = unordered_list_block_to_htmlnode(block)
        expected = ParentNode("ul", [
            ParentNode("li", [LeafNode(None, "buy milk")]),
            ParentNode("li", [LeafNode(None, "buy "), LeafNode("i", "cereal")])
            ])
        self.assertEqual(node, expected)

    def test_ordered_list_block_to_htmlnode(self):
        block = "1. *item* 1\n2. item 2"
        node = ordered_list_block_to_htmlnode(block)
        expected = ParentNode("ol", [
            ParentNode("li", [LeafNode("i", "item"), LeafNode(None, " 1")]),
            ParentNode("li", [LeafNode(None, "item 2")])
            ])
        self.assertEqual(node, expected)

    def test_markdown_to_html_node(self):
        markdown = """
# *this* is a **lv.1** heading

```
print("this is code")
some_function()
```

this is a [link](https://www.boot.dev)
and this is an image ![image](./img/image1.png)

> some quote
> another quote

### heading lv. 3

- *buy* milk
- *buy* cereal
        """
        expected = ParentNode("div", [
            ParentNode("h1", [
                LeafNode("i", "this"),
                LeafNode(None, " is a "),
                LeafNode("b", "lv.1"),
                LeafNode(None, " heading")
                ]),
            ParentNode("pre", [
                ParentNode("code", [
                    LeafNode(None, "print(\"this is code\")\nsome_function()")
                    ])
                ]),
            ParentNode("p", [
                LeafNode(None, "this is a "),
                LeafNode("a", "link", {"href": "https://www.boot.dev"}),
                LeafNode(None, " and this is an image "),
                LeafNode("img", "", {"src": "./img/image1.png", "alt": "image"})
                ]),
            ParentNode("blockquote", [
                LeafNode(None, "some quote another quote")
                ]),
            ParentNode("h3", [
                LeafNode(None, "heading lv. 3")
                ]),
            ParentNode("ul", [
                ParentNode("li", [
                    LeafNode("i", "buy"),
                    LeafNode(None, " milk")
                    ]),
                ParentNode("li", [
                    LeafNode("i", "buy"),
                    LeafNode(None, " cereal")
                    ])
                ])
            ])
        node = markdown_to_html_node(markdown)
        self.assertEqual(node, expected)

        markdown = """
1. put the cereal in a taza
2. then la milk


* more unordered *lists*



just a `paragraph`
with **multiple** lines

and bla bla bla
        """
        expected = ParentNode("div", [
            ParentNode("ol", [
                ParentNode("li", [
                    LeafNode(None, "put the cereal in a taza")
                    ]),
                ParentNode("li", [
                    LeafNode(None, "then la milk")
                    ])
                ]),
            ParentNode("ul", [
                ParentNode("li", [
                    LeafNode(None, "more unordered "),
                    LeafNode("i", "lists")
                    ]),
                ]),
            ParentNode("p", [
                LeafNode(None, "just a "),
                LeafNode("code", "paragraph"),
                LeafNode(None, " with "),
                LeafNode("b", "multiple"),
                LeafNode(None, " lines")
                ]),
            ParentNode("p", [LeafNode(None, "and bla bla bla")])
            ])
        node = markdown_to_html_node(markdown)
        self.assertEqual(node, expected)


if __name__ == "__main__":
    unittest.main()
