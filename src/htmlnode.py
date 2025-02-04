from src.textnode import *


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, properties=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.properties = properties

    def to_html(self):
        raise NotImplementedError

    def properties_to_html(self):
        if not self.properties:
            return ""
        return " " + " ".join(
            [key + '="' + value + '"' for key, value in self.properties.items()]
        )

    def __repr__(self):
        return f'HTMLNode(tag="{self.tag}", value="{self.value}", children={self.children}, properties={self.properties})'


class LeafNode(HTMLNode):
    def __init__(self, tag, value, properties=None):
        super().__init__(tag, value, None, properties)

    def to_html(self):
        if self.tag == "img":
            return f"<img{self.properties_to_html()}>"
        if not self.value:
            raise ValueError
        if not self.tag:
            return str(self.value)

        # regular text doesn't have a tag
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.properties_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children=None, properties=None):
        super().__init__(tag, None, [], properties)

    def to_html(self):
        if not self.tag:
            raise ValueError
        if not self.children:
            raise ValueError("parent node has children missing")
        children_html = ""
        for child in self.children:
            if isinstance(child, list):
                for grand_child in child:
                    children_html += grand_child.to_html()
            else:
                children_html += child.to_html()

        return f"\n<{self.tag}{self.properties_to_html()}>{children_html}</{self.tag}>"
    
    def add_child(self, child):
        self.children.append(child)
    
    def add_children(self, children):
        self.children.extend(children)


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("text_node text type is not valid")
