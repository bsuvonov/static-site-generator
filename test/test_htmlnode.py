import unittest
from src.html_node import *

class TestHTMLNode(unittest.TestCase):
    
    def test_initialization_valid(self):
        # Test with valid tag, value, and properties
        node = HTMLNode(tag="div", value="Hello", properties={"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.properties, {"class": "container"})
        self.assertIsNone(node.children)

    def test_initialization_with_children(self):
        # Test with children nodes
        child_node = HTMLNode(tag="p", value="Child Node")
        node = HTMLNode(tag="div", value="Parent Node", children=[child_node])
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].value, "Child Node")

    def test_properties_to_html(self):
        # Test the properties_to_html method
        node = HTMLNode(tag="input", value=None, properties={"type": "text", "placeholder": "Enter text"})
        expected_html = ' type="text" placeholder="Enter text"'
        self.assertEqual(node.properties_to_html(), expected_html)

    def test_properties_to_html_empty(self):
        # Test with no properties (should return empty string)
        node = HTMLNode(tag="input", value=None)
        self.assertEqual(node.properties_to_html(), "")

    def test_repr(self):
        # Test the __repr__ method for proper representation
        node = HTMLNode(tag="div", value="Hello", properties={"class": "container"})
        expected_repr = 'HTMLNode(tag="div", value="Hello", children=None, properties={\'class\': \'container\'})'
        self.assertEqual(repr(node), expected_repr)


#    def test_invalid_properties(self):
        # Test if properties is not a dictionary (should raise an exception)
#        with self.assertRaises(TypeError):
#            HTMLNode(tag="div", value="Hello", properties=["invalid", "properties"])

    def test_missing_properties(self):
        # Test if properties is omitted (should default to None)
        node = HTMLNode(tag="div", value="Hello")
        self.assertIsNone(node.properties)
    
    def test_repr_with_children(self):
        # Test __repr__ method with children
        child_node = HTMLNode(tag="p", value="Child Node")
        parent_node = HTMLNode(tag="div", value="Parent Node", children=[child_node])
        expected_repr = 'HTMLNode(tag="div", value="Parent Node", children=[HTMLNode(tag="p", value="Child Node", children=None, properties=None)], properties=None)'
        self.assertEqual(repr(parent_node), expected_repr)


if __name__ == "__main__":
    unittest.main()