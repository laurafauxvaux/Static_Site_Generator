import unittest
from block_parser import (markdown_to_blocks, 
                          block_to_block_type,
                          markdown_to_html_node,
                          BlockType)
from inline_parser import text_to_textnodes

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
 
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md   = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
#### This is a heading with some _italic_

And a little paragraph to ensure the separation
"""
        node = markdown_to_html_node(md)
    
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><h4>This is a heading with some <i>italic</i></h4><p>And a little paragraph to ensure the separation</p></div>",
        )
    
    def test_one_blockquote(self):
        md = """
> Testing quotes
> in a single block
"""
        node = markdown_to_html_node(md)
    
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><blockquote>Testing quotes\nin a single block</blockquote></div>",
        )

    def test_two_blockquotes(self):
        md = """
> Just testing a few quotes.

> A second,

> Why not a **third**?
"""
        node = markdown_to_html_node(md)
    
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><blockquote>Just testing a few quotes.</blockquote><blockquote>A second,</blockquote><blockquote>Why not a <b>third</b>?</blockquote></div>",
        )   

    def unordered_list(self):
        md = """
- This is an unordered list.

- For a _checklist,_ for example
"""
        node = markdown_to_html_node(md)
    
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><ul><li>This is an unordered list.</li><li>For a <i>checklist,</i> for example</li></ul></div>",
        )
    
    def ordered_list(self):
        md = """
1. Open browser

2. Check [link](https://boot.dev)

3. Now get to work
"""
        node = markdown_to_html_node(md)
    
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><ol><li>Open browser</li><li>Check <a href='https://boot.dev'>link</a></li><li>Now get to work</li></ul></div>",
        )