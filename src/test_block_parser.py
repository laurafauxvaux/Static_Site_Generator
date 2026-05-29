import unittest
from block_parser import (markdown_to_blocks, 
                          block_to_block_type,
                          BlockType)

class TestBlockParser(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )
    
    def test_markdown_to_blocks_excessive_newline(self):
        md = """
- This is
- a list


and an excessive newline
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,
                         ["- This is\n- a list",
                          "and an excessive newline",
                          ],
                         )
    
    def test_markdown_to_blocks_strips_only_outer_whitespaces(self):
        md = "   This is a text with excessive    whitespace    "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,
                         ["This is a text with excessive    whitespace"])
    

    def test_block_to_block_type_heading(self):
        md = "#### This is a heading"
        self.assertEqual(block_to_block_type(md), BlockType.HEADING)
    
    def test_block_to_block_type_invalid_heading(self):
        md = "####### This is an invalid heading"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_empty_heading(self):
        md = "## "
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_code(self):
        md = """```
This is a code block
```"""
        self.assertEqual(block_to_block_type(md), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        md = """>This is a quote without whitespace
> Including whitespace"""
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)
    
    def test_block_to_block_type_invalid_quote(self):
        md = """>This is a quote
And this is not"""
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_empty_quote(self):
        md = "> "
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        md = """- This is a list
- that is unordered"""
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_invalid_unordered(self):
        md = """- This is a list
rendered invalid"""
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_ordered(self):
        md = """1. This is a list
2. With a numerical order
99. But the rule is 1 by 1"""
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph(self):
        md = "This is a basic text pararaph."
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_empty_paragraph(self):
        md = ""
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)


    
    