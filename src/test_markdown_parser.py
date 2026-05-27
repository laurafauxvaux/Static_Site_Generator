import unittest
from markdown_parser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

class TestMarkdownParser(unittest.TestCase):
    def test_split_bold_text(self):
        nodes = [TextNode("This is plain text", TextType.TEXT),
                 TextNode("This is **bold text**", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("This is plain text", TextType.TEXT, None),
                         TextNode("This is ", TextType.TEXT, None),
                         TextNode("bold text", TextType.BOLD, None),
                         TextNode("", TextType.TEXT, None)
                         ])
    
    def test_split_italic_text(self):
        nodes = [TextNode("This is plain text", TextType.TEXT),
                 TextNode("This is _italic text_", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(result, [TextNode("This is plain text", TextType.TEXT, None),
                         TextNode("This is ", TextType.TEXT, None),
                         TextNode("italic text", TextType.ITALIC, None),
                         TextNode("", TextType.TEXT, None)
                         ])
        
    def test_split_code_text(self):
        nodes = [TextNode("This is plain text", TextType.TEXT),
                    TextNode("This is `code`", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [TextNode("This is plain text", TextType.TEXT, None),
                            TextNode("This is ", TextType.TEXT, None),
                            TextNode("code", TextType.CODE, None),
                            TextNode("", TextType.TEXT, None)
                            ])
    
    def test_err_delimiter_not_str(self):
        with self.assertRaises(ValueError):
            nodes = [TextNode("This is plain text", TextType.TEXT),
                    TextNode("This is `code`", TextType.TEXT)]
            split_nodes_delimiter(nodes, 0, TextType.CODE)

    def test_err_delimiter_not_closed(self):
        with self.assertRaises(Exception):
            nodes = [TextNode("This is plain text", TextType.TEXT),
                    TextNode("This is **bold text", TextType.TEXT)]
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

    def test_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), and this is a ![picture](cat.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("picture", "cat.png")], matches)
    
    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://google.com)")
        self.assertListEqual([("link", "https://google.com")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://google.com), you may also use [second_link](https://yahoo.fr)")
        self.assertListEqual([("link", "https://google.com"), ("second_link", "https://yahoo.fr")], matches)

    def test_extract_markdown_image_without_url(self):
        matches = extract_markdown_images("![image]")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_lookbehind(self):
        matches = extract_markdown_links("[url](https://google.com), ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("url", "https://google.com")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),],new_nodes,)

    def test_split_images_without_image(self):
        node = TextNode("This is text without an image",TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text without an image", TextType.TEXT),],new_nodes,)
    
    def test_split_images_only_images(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),],new_nodes,)
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://google.com) and another [second link](https://yahoo.fr)",
            TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is text with a ", TextType.TEXT),
             TextNode("link", TextType.LINK, "https://google.com"),
             TextNode(" and another ", TextType.TEXT),
             TextNode("second link", TextType.LINK, "https://yahoo.fr"),],new_nodes,)

    def test_split_links_without_link(self):
        node = TextNode(
            "This is text without a link",
            TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is text without a link", TextType.TEXT),],
            new_nodes,)
    
    def test_split_links_only_links(self):
        node = TextNode("[link](https://google.com)[second link](https://yahoo.fr)",TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("link", TextType.LINK, "https://google.com"),
                              TextNode("second link", TextType.LINK, "https://yahoo.fr"),],new_nodes,)