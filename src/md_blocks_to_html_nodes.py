from enum import Enum
from src.html_node import *
from src.text_to_text_nodes import *
from src.md_block import *
import re


def process_paragraph(block):
    parent_node = ParentNode("p")
    for line in block.content:
        text_nodes = text_to_text_nodes(line)
        child_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
        parent_node.add_children(child_nodes)
    return parent_node


def process_heading(block):
    line = block.content[0].strip()
    cnt = 0
    for char in line:
        if char == "#":
            cnt += 1
        else:
            break
    if cnt == 0:
        raise Exception("Invalid header text passed, no '#' available in the text")

    line = line[cnt:].strip()
    parent_node = ParentNode(f"h{cnt}")
    text_nodes = text_to_text_nodes(line)
    child_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
    parent_node.add_children(child_nodes)
    return parent_node


def process_unordered_list(block):
    grand_parent = ParentNode("ul")
    for elem in block.content:
        if isinstance(elem, MarkdownBlock):
            child_nodes = md_block_to_html_nodes(elem)
            grand_parent.add_children(child_nodes)
        else:
            elem = elem.strip()
            parent_node = ParentNode("li")
            text = elem[1:].strip()
            if text == "":
                text = SPACE  # empty list item is possible
            text_nodes = text_to_text_nodes(text)
            child_nodes = [
                text_node_to_html_node(text_node) for text_node in text_nodes
            ]
            parent_node.add_children(child_nodes)
            grand_parent.add_child(parent_node)
    return grand_parent


def process_ordered_list(block):
    grand_parent = ParentNode("ol")
    for elem in block.content:
        if isinstance(elem, MarkdownBlock):
            child_nodes = md_block_to_html_nodes(elem)
            grand_parent.add_children(child_nodes)
        else:
            match = re.search(r"\d+\.\s+(.*)", elem.strip())
            text = SPACE  # empty list item is possible
            if match:
                text = match.group(1)
            parent_node = ParentNode("li")
            text_nodes = text_to_text_nodes(text)
            child_nodes = [
                text_node_to_html_node(text_node) for text_node in text_nodes
            ]
            parent_node.add_children(child_nodes)
            grand_parent.add_child(parent_node)
    return grand_parent


def process_code(block):
    grand_parent = ParentNode("pre")
    language = None
    parent_node = ParentNode("code")

    if len(block.content[0].strip()) > 3:
        language = block.content[0].strip()[3:]
        parent_node.set_properties({"class": f"language-{language}"})

    text_nodes = code_to_textnodes(block.content[1:])
    child_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
    parent_node.add_children(child_nodes)
    grand_parent.add_child(parent_node)
    return grand_parent


def process_quote(block):
    parent_node = ParentNode("blockquote")
    for line in block.content:
        line = line.strip()[
            1:
        ].lstrip()  # remove `>` in the beginning and add '\n' at the end
        text_nodes = text_to_text_nodes(line)
        child_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
        parent_node.add_children(child_nodes)
    return parent_node


def md_block_to_html_nodes(block):
    nodes = []

    match block.type:
        case BlockType.PARAGRAPH:
            nodes.append(process_paragraph(block))
        case BlockType.HEADING:
            nodes.append(process_heading(block))
        case BlockType.UNORDERED_LIST:
            nodes.append(process_unordered_list(block))
        case BlockType.ORDERED_LIST:
            nodes.append(process_ordered_list(block))
        case BlockType.CODE:
            nodes.append(process_code(block))
        case BlockType.QUOTE:
            nodes.append(process_quote(block))

    return nodes


def md_to_html_node(blocks):

    root = ParentNode("div")

    for block in blocks:
        node = md_block_to_html_nodes(block)
        root.add_child(node)

    return root
