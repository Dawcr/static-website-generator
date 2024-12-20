import unittest

from text_utils import BlockType
from text_utils import (
    markdown_to_blocks,
    block_to_block_type,
    extract_title,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_example(self):
        text = """# This is a heading
        
        This is a paragraph of text. It has some **bold** and *italic* words inside of it.
        
        * This is the first list item in a list block
        * This is a list item
        * This is another list item"""
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
            markdown_to_blocks(text),
        )
        
    def test_whitespaces(self):
        text = """                     This is a test for whitespaces              
        
        
        
        
        
        
        
        
        
        
        lots of whitespaces                  """
        self.assertListEqual(
            [
                "This is a test for whitespaces",
                "lots of whitespaces",
            ],
            markdown_to_blocks(text),
        )
        
    # boot.dev tests
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )
        
        
class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        text = "#### This is a heading 4"
        self.assertEqual(
            block_to_block_type(text),
            BlockType.HEADING,
        )
        
    def test_code(self):
        text = """```
        This is a block of code
        ```"""
        self.assertEqual(
            block_to_block_type(text),
            BlockType.CODE,
        )
        
        text2 = """```
        This is a block of code
        ``````
        as is this abomination
        ```"""
        self.assertEqual(
            block_to_block_type(text2),
            BlockType.CODE,
        )
    
    def test_quote(self):
        text = """> quote
>quote"""
        self.assertEqual(
            block_to_block_type(text),
            BlockType.QUOTE,
        )
    
    def test_ulist(self):
        text = """- item
- another item
- yet another item"""
        self.assertEqual(
            block_to_block_type(text),
            BlockType.UNORDERED_LIST,
        )
        
        text = """* item
* another item
* yet another item"""
        self.assertEqual(
            block_to_block_type(text),
            BlockType.UNORDERED_LIST,
        )
            
    def test_ordered(self):
        text = """1. this is an ordered list item
2. this is another item"""
        self.assertEqual(
            block_to_block_type(text),
            BlockType.ORDERED_LIST,
        )
            
    def test_normal(self):
        text = "this is just plain old text"
        self.assertEqual(
            block_to_block_type(text),
            BlockType.PARAGRAPH,
        )        
        
    # boot.dev tests
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        
class TestExtractTitle(unittest.TestCase):
    def test_example(self):
        text = "# Hello"
        self.assertEqual(
            extract_title(text),
            "Hello",
        )
        
    def test_exception(self):
        text = "### Hello"
        with self.assertRaisesRegex(ValueError, "Missing h1 header"):
            extract_title(text)
        
        
if __name__ == "__main__":
    unittest.main()