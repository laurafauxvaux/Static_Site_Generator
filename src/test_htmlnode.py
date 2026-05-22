import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "research here", None, {"href": "https://www.google.com","target": "_blank",})
        node2 = HTMLNode("p", "research here", None, {"href": "https://www.google.com","target": "_blank",})
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = HTMLNode("p", "research here", None, {"href": "https://www.google.com","target": "_blank",})
        node2 = HTMLNode("p", "or over there", None, {"href": "https://www.google.com","target": "_blank",})
        self.assertNotEqual(node, node2)
    
    def test_eq_tag(self):
        node = HTMLNode("p")
        node2 = HTMLNode("p")
        self.assertEqual(node, node2)

    def test_eq_value(self):
        node = HTMLNode("p", "hello")
        node2 = HTMLNode("p", "hello")
        self.assertEqual(node, node2)

    def test_eq_children(self):
        node = HTMLNode("p", "hello", [HTMLNode(value="world")])
        node2 = HTMLNode("p", "hello", [HTMLNode(value="world")])
        self.assertEqual(node, node2)

    def test_eq_props(self):
        node = HTMLNode("p", "hello", [HTMLNode(value="world")], {"href": "https://www.google.com","target": "_blank",})
        node2 = HTMLNode("p", "hello", [HTMLNode(value="world")], {"href": "https://www.google.com","target": "_blank",})
        self.assertEqual(node, node2)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Let's research!", {"href": 'https://www.google.com'})
        self.assertEqual(node.to_html(), "<a href='https://www.google.com'>Let's research!</a>")
    
    def test_leaf_to_html_blockquote(self):
        node = LeafNode("blockquote", "This famous quote:", {"class":'quote'})
        self.assertEqual(node.to_html(), "<blockquote class='quote'>This famous quote:</blockquote>")

    def test_no_tag(self):
        node = LeafNode(None, "Winter is coming")
        self.assertEqual(node.to_html(), "Winter is coming")

    def test_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("div", None)
            node.to_html()