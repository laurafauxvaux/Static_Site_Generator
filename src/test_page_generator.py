import unittest
from page_generator import extract_title

class TestPageGenerator(unittest.TestCase):

    def extract_title_two_headings(self):
        md = """
# should only extract h1 heading

### should not extract h3 heading
""" 
        result = extract_title(md)
        self.assertEqual(result, "should only extract h1 heading")
    
    def extract_title_different_blocks(self):
        md = """
Putting some paragraph

- list 1

- list 2

# to check heading
"""
        result = extract_title(md)
        self.assertEqual(result, "to check heading")
    
    def extract_title_err_no_h1(self):
        md = """
### no h1 heading here
"""
        with self.assertRaises(Exception):
            extract_title(md)