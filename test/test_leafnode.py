import unittest
from src.html_node import *


class TestLeafNode(unittest.TestCase):
    
    def test_initialization_valid(self):
        # Test with valid parameters
        node = LeafNode(tag="p", value="Hello, World!", properties={"class": "text"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, World!")
        self.assertEqual(node.properties, {"class": "text"})
        self.assertIsNone(node.children)  # Should be None for LeafNode
    
    def test_to_html_valid(self):
        # Test valid HTML generation
        node = LeafNode(tag="p", value="Hello, World!", properties={"class": "text"})
        expected_html = '<p class="text">Hello, World!</p>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_no_properties(self):
        # Test HTML generation without properties
        node = LeafNode(tag="p", value="Hello, World!")
        expected_html = '<p>Hello, World!</p>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_empty_value(self):
        # Test case where value is empty (should raise ValueError)
        node = LeafNode(tag="p", value="")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag(self):
        # Test case where tag is None (should return value itself)
        node = LeafNode(tag=None, value="Hello, World!")
        self.assertEqual(node.to_html(), "Hello, World!")

    def test_to_html_invalid_value(self):
        # Test case where value is None (should raise ValueError)
        node = LeafNode(tag="p", value=None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr(self):
        # Test the __repr__ method
        node = LeafNode(tag="p", value="Hello, World!", properties={"class": "text"})
        expected_repr = 'HTMLNode(tag="p", value="Hello, World!", children=None, properties={\'class\': \'text\'})'
        self.assertEqual(repr(node), expected_repr)

    def test_repr_no_properties(self):
        # Test __repr__ with no properties
        node = LeafNode(tag="p", value="Hello")
        expected_repr = 'HTMLNode(tag="p", value="Hello", children=None, properties=None)'
        self.assertEqual(repr(node), expected_repr)

    def test_repr_no_value(self):
        # Test __repr__ with no value (but tag exists)
        node = LeafNode(tag="p", value=None)
        expected_repr = 'HTMLNode(tag="p", value="None", children=None, properties=None)'
        self.assertEqual(repr(node), expected_repr)


if __name__ == "__main__":
    unittest.main()
