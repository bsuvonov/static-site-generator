import unittest
from src.code import *

class TestMarkdownExtract(unittest.TestCase):

    def test_extract_markdown_images(self):
        # Test case 1: Normal case with multiple images
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

        # Test case 2: No images in the text
        text = "This is text with no images"
        self.assertEqual(extract_markdown_images(text), [])

        # Test case 3: Empty string
        text = ""
        self.assertEqual(extract_markdown_images(text), [])

        # Test case 4: Only image links, no other text
        text = "![](https://i.imgur.com/aKaOqIh.gif)"
        self.assertEqual(extract_markdown_images(text), [("", "https://i.imgur.com/aKaOqIh.gif")])

        # Test case 5: Image with no alt text
        text = "Check out this image ![](https://i.imgur.com/xyz.jpg)"
        self.assertEqual(extract_markdown_images(text), [("", "https://i.imgur.com/xyz.jpg")])

    def test_extract_markdown_links(self):
        # Test case 1: Normal case with multiple links
        text = "This is text with a link [to example.com](https://www.example.com) and [to youtube](https://www.youtube.com/@exampledotcom)"
        self.assertEqual(extract_markdown_links(text), [("to example.com", "https://www.example.com"), ("to youtube", "https://www.youtube.com/@exampledotcom")])

        # Test case 2: No links in the text
        text = "This is text with no links"
        self.assertEqual(extract_markdown_links(text), [])

        # Test case 3: Empty string
        text = ""
        self.assertEqual(extract_markdown_links(text), [])

        # Test case 4: Only links, no other text
        text = "[Google](https://www.google.com)"
        self.assertEqual(extract_markdown_links(text), [("Google", "https://www.google.com")])

        # Test case 5: Link with no anchor text
        text = "Check this [example](https://www.example.com)"
        self.assertEqual(extract_markdown_links(text), [("example", "https://www.example.com")])

if __name__ == '__main__':
    unittest.main()
