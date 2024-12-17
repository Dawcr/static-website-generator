import unittest

from textnode import TextNode, TextType, text_node_to_html_node

from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("This is a text node link", TextType.LINK, None)
        node4 = TextNode("This is a text node link", TextType.LINK, None)
        self.assertEqual(node3, node4)
        
        node5 = TextNode("This is a text node image", TextType.IMAGE, "https://example.com/image")
        node6 = TextNode("This is a text node image", TextType.IMAGE, "https://example.com/image")
        self.assertEqual(node5, node6)
        
        self.assertNotEqual(node4, node5)
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node2, node5)
        
        self.assertEqual(
            node.__repr__(),
            "TextNode(This is a text node, bold, None)"
        )

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

if __name__ == "__main__":
    unittest.main()