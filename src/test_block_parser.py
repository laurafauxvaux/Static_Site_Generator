import unittest
from block_parser import markdown_to_blocks

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
    

        