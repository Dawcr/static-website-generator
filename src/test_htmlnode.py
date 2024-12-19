import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="link", props={"rel":"stylesheet", "href":"styles.css"})
        html = " rel=\"stylesheet\" href=\"styles.css\""
        self.assertEqual(node.props_to_html(), html)
        
        node2 = HTMLNode(tag="a", value="Go to Google.com", props={"href": "https://www.google.com", "target": "_blank"})
        html2 = " href=\"https://www.google.com\" target=\"_blank\""
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
        
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(
            node.to_html(),
            "<p>This is a paragraph of text.</p>"
        )
        
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node2.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )
        
        with self.assertRaisesRegex(ValueError, "Leaf node has no value"):
            node3 = LeafNode(None, None)
            node3.to_html()
            
    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
        
    def test_leafnode_repr(self):
        node = LeafNode("p", "Hello world!")
        self.assertEqual(
            node.__repr__(),
            "LeafNode(p, Hello world!, None)"
        )
        
    def test_to_html_parentnode(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
        
        with self.assertRaisesRegex(ValueError, "Parent node has no tag"):
            node2 = ParentNode(
                None,
                [
                    LeafNode(None, "Normal text")
                ],
                )
            node2.to_html()
        
        with self.assertRaisesRegex(ValueError, "Parent node has no children"):
            node3 = ParentNode(
                "p",
                None
            )
            node3.to_html()
            
        node4 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "Normal text"),
                        ParentNode(
                            "p",
                            [
                                LeafNode("i", "italic text"),
                            ]
                        ),
                    ]
                )
            ],
        )
        
        self.assertEqual(
            node4.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text<p>Normal text<p><i>italic text</i></p></p></p>"
        )
        
        with self.assertRaisesRegex(ValueError, "Leaf node has no value"):
            node4 = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                    ParentNode(
                        "p",
                        [
                            LeafNode(None, "Normal text"),
                            ParentNode(
                                "p",
                                [
                                    LeafNode(None, None),
                                ]
                            ),
                        ]
                    )
                ],
            )
            node4.to_html() 
            
    # boot.dev tests
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
        
        
if __name__ == "__main__":
    unittest.main()