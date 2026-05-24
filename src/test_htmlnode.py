import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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
        node = LeafNode(None, "One ring to rule them all")
        self.assertEqual(node.to_html(), "One ring to rule them all")

    def test_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("div", None)
            node.to_html()

    class TestParentNode(unittest.TestCase):
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

        def test_to_html_with_nested_parents(self):
            leaf_node = LeafNode("blockquote", "This famous quote:", {"class":'quote'})
            small_node = ParentNode("small", [leaf_node])
            i_node = ParentNode("i", [small_node])
            a_node = ParentNode("a", [i_node])
            b_node = ParentNode("b", [a_node])
            self.assertEqual(
                b_node.to_html(),
                "<b><a><i><small><blockquote class='quote'>This famous quote:</blockquote></small></i></a></b>",
            )
        
        def test_to_html_with_multiple_children(self):
            child_node_1= LeafNode("main", "Best quotes")
            child_node_2= LeafNode("article", "LOTR")
            child_node_3 = LeafNode("blockquote", "This famous quote:", {"class":'quote'})           
            parent_node = ParentNode("b", [child_node_1, child_node_2, child_node_3])
            self.assertEqual(parent_node.to_html(),
                             "<b><main>Best quotes</main><article>LOTR</article><blockquote class='quote'>This famous quote:</blockquote></b>")
            
        def test_to_html_with_no_children(self):
            with self.assertRaises(ValueError):
                parent_node = ParentNode("div", None, None)
                parent_node.to_html()
        
        def test_to_html_with_no_tag(self):
            with self.assertRaises(ValueError):
                parent_node = ParentNode(None, LeafNode("p", "hello"))
                parent_node.to_html()
        
        def test_parent_with_props(self):
            child_node = LeafNode("i", "hello")
            parent = ParentNode("div", [child_node], {"class":'container'})
            self.assertEqual(parent.to_html(), "<div class='container'><i>hello</i></div>")