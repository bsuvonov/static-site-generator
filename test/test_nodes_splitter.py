import unittest
from src.text_node import TextNode, TextType
from src.text_to_text_nodes import *


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_basic_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**")
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_basic_italic(self):
        node = TextNode("This is an *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*")
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_basic_code(self):
        node = TextNode("This is a `code block` in a sentence", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`")
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" in a sentence", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_delimiters(self):
        node = TextNode("This is *italic* and **bold** and `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*")
        new_nodes = split_nodes_delimiter(new_nodes, "**")
        new_nodes = split_nodes_delimiter(new_nodes, "`")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_unbalanced_delimiters(self):
        node = TextNode("This is **bold text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**")
        expected = [TextNode("This is **bold text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_no_delimiters(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*")
        expected = [
            TextNode("Just plain text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)

    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*")
        expected = [
            TextNode("", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)

    def test_edge_case_consecutive_delimiters(self):
        node = TextNode("This is **bold**italic**text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**")
        new_nodes = split_nodes_delimiter(new_nodes, "*")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("italic**text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_matching_delimiter(self):
        node = TextNode("No delimiter text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "#")
        expected = [
            TextNode("No delimiter text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
