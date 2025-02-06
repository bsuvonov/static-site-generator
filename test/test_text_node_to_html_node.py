import unittest
from src.html_node import *


class TestTextNodeToHtmlNode(unittest.TestCase):

    def test_text_node_to_html_node_text(self):
        # Test case for normal text type (TextType.TEXT)
        text_node = TextNode("This is normal text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "This is normal text")
    
    def test_text_node_to_html_node_bold(self):
        # Test case for bold text type (TextType.BOLD)
        text_node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<b>This is bold text</b>')
    
    def test_text_node_to_html_node_italic(self):
        # Test case for italic text type (TextType.ITALIC)
        text_node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<i>This is italic text</i>')
    
    def test_text_node_to_html_node_code(self):
        # Test case for code text type (TextType.CODE)
        text_node = TextNode("This is code text", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<code>This is code text</code>')
    
    def test_text_node_to_html_node_link(self):
        # Test case for link text type (TextType.LINK)
        text_node = TextNode("This is a link", TextType.LINK, url="http://example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<a href="http://example.com">This is a link</a>')

    def test_text_node_to_html_node_image(self):
        # Test case for image text type (TextType.IMAGE)
        text_node = TextNode("This is an image", TextType.IMAGE, url="http://example.com/image.jpg")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<img src="http://example.com/image.jpg" alt="This is an image">')

    def test_text_node_to_html_node_invalid_type(self):
        # Test case for invalid text type (should raise an exception)
        text_node = TextNode("Invalid type", "INVALID_TYPE")
        with self.assertRaises(Exception):
            text_node_to_html_node(text_node)

if __name__ == "__main__":
    unittest.main()
