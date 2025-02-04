from enum import Enum
import os
from src.htmlnode import *
from src.code import *

class BlockType(Enum):
    HEADING = "BlockType.HEADING"
    LIST = "BlockType.LIST"
    ORDERED_LIST = "BlockType.ORDERED_LIST"
    UNORDERED_LIST = "BlockType.UNORDERED_LIST"
    QUOTE = "BlockType.QUOTE"
    CODE = "BlockType.CODE"
    PARAGRAPH = "BlockType.PARAGRAPH"


class MarkdownBlock:
    def __init__(self, type, content, children=None):
        self.type = type
        self.content = content

    def __repr__(self):
        repr = f"MarkdownBlock(type={self.type}, content:"
        for elem in self.content:
            repr += f'\n\t{elem}' 
        repr += '\n)'
        return repr 


def identify_block_type(line):

    line = line.strip()
    if line == "":      # This condition is true only when the function is called by the while loop condition of code_block_helper, so it's fine to return PARAGRAPH
        return BlockType.PARAGRAPH

    if line.startswith("#"):
        return BlockType.HEADING
    elif (
        line.startswith("- ")
        or line.startswith("* ")
        or (line[0] in "0123456789" and "." in line[0:3])
    ):
        return BlockType.LIST
    elif line.startswith("```") or line.startswith("~~~"):
        return BlockType.CODE
    elif line.startswith("> "):
        return BlockType.QUOTE
    else:
        return BlockType.PARAGRAPH





def paragraph_block_helper(lines, index):

    content = []
    content.append(lines[index])
    index += 1
    while (
        index < len(lines)
        and lines[index].strip() != ""
        and identify_block_type(lines[index]) == BlockType.PARAGRAPH
    ):
        content.append(lines[index].strip())
        index += 1
    
    return MarkdownBlock(BlockType.PARAGRAPH, content), index


def header_block_helper(lines, index):
    content = []
    content.append(lines[index])
    return MarkdownBlock(BlockType.HEADING, content), index


def code_block_helper(lines, index):
    content = []
    content.append(lines[index])
    index += 1
    while (
        index < len(lines)
        and identify_block_type(lines[index]) != BlockType.CODE
    ):
        content.append(lines[index])
        index += 1
    
    return MarkdownBlock(BlockType.CODE, content), index



def quote_block_helper(lines, index):
    content = []
    content.append(lines[index])
    index += 1
    while (
        index < len(lines)
        and lines[index].strip() != ""
        and identify_block_type(lines[index])
        in [BlockType.PARAGRAPH, BlockType.QUOTE]
    ):
        content.append(lines[index])
        index += 1

    return MarkdownBlock(BlockType.QUOTE, content), index




def list_block_helper(lines, index, spaces, n_of_spaces):
    content = []
    content.append(lines[index])
#    print("being appended to content", lines[index])
    index += 1
#    print("now comes", lines[index], f"spaces{spaces*n_of_spaces}tugadi")
#    print(f"spaces:{spaces},n_of_spaces:{n_of_spaces}")
    while (
        index < len(lines)
        and lines[index].startswith(spaces*n_of_spaces)     # we should not jump to parent section when child section ends
        and (identify_block_type(lines[index]) == BlockType.LIST
             or lines[index].startswith(spaces*(n_of_spaces+1)))
    ):
#        print("n_of_spaces:", n_of_spaces, f"spaces:{spaces}cont:{lines[index]}")

        if lines[index].startswith(spaces*(n_of_spaces+1)):
            # identify how many space character is one tab
            if n_of_spaces == 0:
                spaces = " "*(len(lines[index])-len(lines[index].lstrip()))
                child_block, index = retrieve_block(lines, index, spaces, 1)
            else:
                child_block, index = retrieve_block(lines, index, spaces, n_of_spaces+1)
            content.append(child_block)

        else:
            content.append(lines[index])
        index += 1
    
    return MarkdownBlock(BlockType.LIST, content), index




def retrieve_block(lines, index, spaces, n_of_spaces):
    
    # if there is too much indentation, line is considered as paragraph
    if lines[index].startswith(spaces*(n_of_spaces+2)):
        block_type = BlockType.PARAGRAPH
    else:
        block_type = identify_block_type(lines[index])
    block = None

    match block_type:
        case BlockType.PARAGRAPH:
            block, index = paragraph_block_helper(lines, index)

        case BlockType.HEADING:
            block, index = header_block_helper(lines, index)

        case BlockType.LIST:
            block, index = list_block_helper(lines, index, spaces, n_of_spaces)

        case BlockType.CODE:
            block, index = code_block_helper(lines, index)

        case BlockType.QUOTE:
            block, index = quote_block_helper(lines, index)
    
    return block, index





# `spaces` is used for LIST type to parse child sections
def split_blocks(markdown):

    blocks = []
    lines = markdown.split('\n')
    index = 0

    while index < len(lines):
        # markdown ignores whitespace between text
        if lines[index].strip()=="":
            index += 1
            continue
        block, index = retrieve_block(lines, index, " "*2, 0)

        index += 1
        blocks.append(block)

    return blocks                



def process_markdown():

    md = open("./mds/penguins.md", "r")
    md_content = md.read()
    md.close()

    blocks = split_blocks(md_content)

    print()
    print()
    print()
    

    for block in blocks:
        print()
        print(block)

#    markdown_to_html_node(blocks)

    


















def markdown_to_html_node(blocks):

    root = ParentNode("div")
    
    for block in blocks:
        match block.type:
            case BlockType.PARAGRAPH:
                for line in block.content:
                    html_parent = ParentNode("p", [])
                    text_nodes = text_to_textnodes(line)
                    for text_node in text_nodes:
                        html_leaf = text_node_to_html_node(text_node)
                        html_parent.add_child(html_leaf)
                    root.add_child(html_parent)
            
            case BlockType.HEADING:
                for line in block.content:
                    header_type = len(line.split()[0])
                    html_parent = ParentNode(f"h{header_type}")
                    text_nodes = text_to_textnodes(line)
                    for text_node in text_nodes:
                        html_leaf = text_node_to_html_node(text_node)
                        html_parent.add_child(html_leaf)
                    root.add_child(html_parent)
            