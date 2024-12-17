import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="link", props={"rel":"stylesheet", "href":"styles.css"})
        html = "rel: \"stylesheet\" href: \"styles.css\""
        self.assertEqual(node.props_to_html(), html)
        
        node2 = HTMLNode(tag="a", value="Go to Google.com", props={"href": "https://www.google.com", "target": "_blank"})
        html2 = "href: \"https://www.google.com\" target: \"_blank\""
        self.assertEqual(node2.props_to_html(), html2)
        
        self.assertNotEqual(node.props_to_html(), node2.props_to_html())
        
        node3 = HTMLNode()
        
        self.assertEqual(node3.props_to_html(), "")
        
    def test_values(self):
        node = HTMLNode(tag="div", value="hello world")
        self.assertEqual(
            node.tag,
            "div"
        )
        self.assertEqual(
            node.value,
            "hello world"
        )
        self.assertEqual(
            node.children,
            None
        )
        self.assertEqual(
            node.props,
            None
        )
        
    def test_repr(self):
        node = HTMLNode(
            "p",
            "Lorem ipsum",
            None,
            {"class" : "placeholder"}
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, Lorem ipsum, children: None, {'class': 'placeholder'})"
        )
        node2 = HTMLNode(
            tag="p",
            value="Lorem ipsum dolor",
            props={"class" : "placeholder"}
        )
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()