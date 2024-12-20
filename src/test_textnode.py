import unittest

from textnode import TextNode, TextType


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
            "TextNode(This is a text node, bold, None)",
        )


if __name__ == "__main__":
    unittest.main()