import unittest
from src.text_to_text_nodes import *
from src.html_node import *
from src.text_node import *


class TestMarkdownToTextNodes(unittest.TestCase):

    def test_text_to_textnodes(self):
        # Test case 1: Normal case with bold, italic, code, image, and link
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        self.assertEqual(text_to_text_nodes(text), expected_output)

        # Test case 2: No markdown formatting
        text = "This is just plain text."
        expected_output = [
            TextNode("This is just plain text.", TextType.TEXT)
        ]
        self.assertEqual(text_to_text_nodes(text), expected_output)

        # Test case 3: Only bold formatting
        text = "**bold text**"
        expected_output = [
            TextNode("bold text", TextType.BOLD)
        ]
        self.assertEqual(text_to_text_nodes(text), expected_output)

        # Test case 4: Only italic formatting
        text = "*italic text*"
        expected_output = [
            TextNode("italic text", TextType.ITALIC)
        ]
        self.assertEqual(text_to_text_nodes(text), expected_output)

        # Test case 5: Only code block formatting
        text = "`code block`"
        expected_output = [
            TextNode("code block", TextType.CODE)
        ]
        self.assertEqual(text_to_text_nodes(text), expected_output)

        # Test case 6: Only image formatting
        text = "![image](https://example.com/image.jpg)"
        expected_output = [
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg")
        ]
        self.assertEqual(text_to_text_nodes(text), expected_output)

        # Test case 7: Only link formatting
        text = "[link](https://example.com)"
        expected_output = [
            TextNode("link", TextType.LINK, "https://example.com")
        ]
        self.assertEqual(text_to_text_nodes(text), expected_output)

        # Test case 8: Empty string
        text = ""
        expected_output = []
        self.assertEqual(text_to_text_nodes(text), expected_output)

        # Test case 9: Multiple formats together
        text = "This is **bold** and *italic* and `code` and ![image](https://example.com/image.jpg) and [link](https://example.com)"
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com")
        ]
        self.assertEqual(text_to_text_nodes(text), expected_output)

        # Test case 10: Image without alt text
        text = "![image](https://example.com/image.jpg)"
        expected_output = [
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg")
        ]
        self.assertEqual(text_to_text_nodes(text), expected_output)

        # Test case 11: Link with no anchor text
        text = "[ ](https://example.com)"
        expected_output = []
        print(text_to_text_nodes(text))
        self.assertEqual(text_to_text_nodes(text), expected_output)


if __name__ == '__main__':
    unittest.main()
