import unittest

from node_utils import text_node_to_html_node, split_nodes_delimiter

from textnode import TextType, TextNode
from htmlnode import LeafNode


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_node(self):
        text_node1 = TextNode("normal text", TextType.TEXT)
        node1 = text_node_to_html_node(text_node1)
        self.assertIsInstance(node1, LeafNode)
        self.assertEqual(
            node1.__repr__(),
            "LeafNode(None, normal text, None)"
        )
        self.assertEqual(
            node1.to_html(),
            "normal text"
        )
        
        text_node2 = TextNode("bold text", TextType.BOLD)
        node2 = text_node_to_html_node(text_node2)
        self.assertIsInstance(node2, LeafNode)
        self.assertEqual(
            node2.__repr__(),
            "LeafNode(b, bold text, None)"
        )
        self.assertEqual(
            node2.to_html(),
            "<b>bold text</b>"
        )
        
        text_node3 = TextNode("italic text", TextType.ITALIC)
        node3 = text_node_to_html_node(text_node3)
        self.assertIsInstance(node3, LeafNode)
        self.assertEqual(
            node3.__repr__(),
            "LeafNode(i, italic text, None)"
        )
        self.assertEqual(
            node3.to_html(),
            "<i>italic text</i>"
        )
        
        text_node4 = TextNode("code", TextType.CODE)
        node4 = text_node_to_html_node(text_node4)
        self.assertIsInstance(node4, LeafNode)
        self.assertEqual(
            node4.__repr__(),
            "LeafNode(code, code, None)"
        )
        self.assertEqual(
            node4.to_html(),
            "<code>code</code>"
        )
        
        text_node5 = TextNode("click here", TextType.LINK, "https://www.google.com")
        node5 = text_node_to_html_node(text_node5)
        self.assertIsInstance(node5, LeafNode)
        self.assertEqual(
            node5.__repr__(),
            "LeafNode(a, click here, {'href': 'https://www.google.com'})"
        )
        self.assertEqual(
            node5.to_html(),
            '<a href="https://www.google.com">click here</a>'
        )
        
        text_node6 = TextNode("an image of a cat", TextType.IMAGE, "https://www.example.com/cat.jpeg")
        node6 = text_node_to_html_node(text_node6)
        self.assertIsInstance(node6, LeafNode)
        self.assertEqual(
            node6.__repr__(),
            "LeafNode(img, , {'src': 'https://www.example.com/cat.jpeg', 'alt': 'an image of a cat'})"
        )
        self.assertEqual(
            node6.to_html(),
            '<img src="https://www.example.com/cat.jpeg" alt="an image of a cat" />'
        )
        
        with self.assertRaisesRegex(ValueError, "Trying to convert text node with invalid text type"):
            text_node7 = TextNode("error", "tiny")
            text_node_to_html_node(text_node7)        
            
    # boot.dev tests
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")


class TestSplitNodeDelimiter(unittest.TestCase):
    def test_texttypecode(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ]   
        )
    
    def test_startingdelimiter(self):
        node = TextNode("*Bold* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT)
            ]
        )
        
    # boot.dev tests
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()