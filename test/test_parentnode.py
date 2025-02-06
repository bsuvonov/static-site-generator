import unittest
from src.html_node import *


class TestHTMLNodes(unittest.TestCase):

    def test_leaf_node_valid(self):
        # Test LeafNode with valid tag, value, and properties
        node = LeafNode(tag="b", value="Bold text", properties={"class": "bold"})
        self.assertEqual(node.to_html(), '<b class="bold">Bold text</b>')

    def test_leaf_node_no_properties(self):
        # Test LeafNode with no properties
        node = LeafNode(tag="b", value="Bold text")
        self.assertEqual(node.to_html(), '<b>Bold text</b>')

    def test_leaf_node_empty_value(self):
        # Test LeafNode with empty value (should raise ValueError)
        node = LeafNode(tag="b", value="")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_node_no_tag(self):
        # Test LeafNode with no tag (should return value itself)
        node = LeafNode(tag=None, value="Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_parent_node_valid(self):
        # Test ParentNode with valid children (LeafNode instances)
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode("i", "Italic text"),
                LeafNode("u", "Underlined text")
            ]
        )
        expected_html = '<p><b>Bold text</b><i>Italic text</i><u>Underlined text</u></p>'
        self.assertEqual(node.to_html(), expected_html)

    def test_parent_node_no_tag(self):
        # Test ParentNode with no tag (should raise ValueError)
        node = ParentNode(tag=None, children=[])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_node_missing_children(self):
        # Test ParentNode with missing children (should raise ValueError)
        node = ParentNode(tag="div", children=None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_node_no_children(self):
        # Test ParentNode with no children (should raise ValueError)
        node = ParentNode(tag="div", children=[])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_node_with_nested_parent_nodes(self):
        # Test ParentNode with nested ParentNode objects as children
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        LeafNode("p", "Section paragraph 1"),
                        LeafNode("p", "Section paragraph 2")
                    ]
                ),
                LeafNode("h1", "Main heading")
            ]
        )
        expected_html = (
            '<div>'
            '<section><p>Section paragraph 1</p><p>Section paragraph 2</p></section>'
            '<h1>Main heading</h1>'
            '</div>'
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_parent_node_with_mixed_children(self):
        # Test ParentNode with a mix of LeafNode and ParentNode children
        node = ParentNode(
            "div",
            [
                LeafNode("p", "Paragraph 1"),
                ParentNode("section", [LeafNode("h1", "Section Heading")]),
                LeafNode("p", "Paragraph 2")
            ]
        )
        expected_html = (
            '<div>'
            '<p>Paragraph 1</p>'
            '<section><h1>Section Heading</h1></section>'
            '<p>Paragraph 2</p>'
            '</div>'
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_parent_node_with_invalid_children(self):
        # Test ParentNode with invalid children (non-LeafNode objects)
        node = ParentNode(
            "div",
            ["This is a string instead of a LeafNode"]
        )
        with self.assertRaises(AttributeError):
            node.to_html()

    def test_parent_node_with_multiple_nested_levels(self):
        # Test deeply nested ParentNode objects
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        ParentNode(
                            "article",
                            [
                                LeafNode("h2", "Article Title"),
                                LeafNode("p", "Article content")
                            ]
                        ),
                        LeafNode("p", "Section content")
                    ]
                ),
                LeafNode("footer", "Footer content")
            ]
        )
        expected_html = (
            '<div>'
            '<section>'
            '<article><h2>Article Title</h2><p>Article content</p></article>'
            '<p>Section content</p>'
            '</section>'
            '<footer>Footer content</footer>'
            '</div>'
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_parent_node_with_no_tag_and_no_children(self):
        # Test ParentNode with no tag and no children (should raise ValueError)
        node = ParentNode(tag=None, children=None)
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()

