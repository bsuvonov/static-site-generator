import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD, 'https')
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

        # Different text content
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

        # Different text type
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)  # Assuming TextType.ITALIC exists
        self.assertNotEqual(node, node2)

        # Different URL (another case)
        node = TextNode("This is a text node", TextType.BOLD, 'https://example.com')
        node2 = TextNode("This is a text node", TextType.BOLD, 'https://another-url.com')
        self.assertNotEqual(node, node2)



if __name__ == "__main__":
    unittest.main()