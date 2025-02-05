from enum import Enum
import os
import re
from src.htmlnode import *
from src.code import *
from src.blocks_to_html_nodes import markdown_block_to_html_nodes

class BlockType(Enum):
    HEADING = "BlockType.HEADING"
    ORDERED_LIST = "BlockType.ORDERED_LIST"
    UNORDERED_LIST = "BlockType.UNORDERED_LIST"
    QUOTE = "BlockType.QUOTE"
    CODE = "BlockType.CODE"
    PARAGRAPH = "BlockType.PARAGRAPH"

SPACE = " "


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

    line = line.lstrip()
    if line == "":      # This condition is true only when the function is called by the while loop condition of code_block_helper, so it's fine to return PARAGRAPH
        return BlockType.PARAGRAPH

    if line.startswith("#"):
        return BlockType.HEADING
    elif (
        line.startswith("- ")
        or line.startswith("* ")):
        return BlockType.UNORDERED_LIST
    elif line[0] in "0123456789" and "." in line[0:3]:
        return BlockType.ORDERED_LIST
    elif line.startswith("```") or line.startswith("~~~"):
        return BlockType.CODE
    elif line.startswith(">"):
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
    index += 1
    return MarkdownBlock(BlockType.HEADING, content), index


def code_block_helper(lines, index):
    content = [lines[index]]
    index += 1
    while (
        index < len(lines)
        and identify_block_type(lines[index]) != BlockType.CODE
    ):
        content.append(lines[index])
        index += 1
    
    return MarkdownBlock(BlockType.CODE, content), index+1  # exclude the ending ```



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




def list_block_helper(lines, index, spaces, n_of_spaces, block_type):
    print("inside block_helper()", lines[index])

    content = []
    content.append(lines[index])
    old_index = index
    index += 1
    print("inside block_helper()", lines[index] + spaces + str(n_of_spaces))


    while (
        index < len(lines)
        and (lines[index].startswith(spaces*n_of_spaces)     # we should not jump to parent section when child section ends
        and (identify_block_type(lines[index]) == block_type or lines[index].startswith(spaces*(n_of_spaces+1)))
        or lines[index] == "")
    ):
        print("inside while:",lines[index], block_type)
        if lines[index] == "":      # if line is empty
            index+=1
        elif lines[index].startswith(spaces*(n_of_spaces)+2*SPACE):     # if line is the beginning of subsection
            print("passing to child:", lines[index])
            # identify how many space characters make up one tab
            if n_of_spaces == 0:
                spaces = SPACE*(len(lines[index])-len(lines[index].lstrip()))
                child_block, index = retrieve_block(lines, index, spaces, 1)
            else:
                child_block, index = retrieve_block(lines, index, spaces, n_of_spaces+1)
            #print("child returned, next line:", lines[index])
            content.append(child_block)

        else:       # if line is a list item
            content.append(lines[index])
            index += 1
#        index += 1

    return MarkdownBlock(block_type, content), index




def retrieve_block(lines, index, spaces, n_of_spaces):

    print("inside retrieve:", lines[index])
    
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

        case BlockType.ORDERED_LIST:
            block, index = list_block_helper(lines, index, spaces, n_of_spaces, block_type)

        case BlockType.UNORDERED_LIST:
            block, index = list_block_helper(lines, index, spaces, n_of_spaces, block_type)

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
        block, index = retrieve_block(lines, index, SPACE*2, 0)
        

#        index += 1
        blocks.append(block)

    return blocks                



def process_markdown():

    md = open("./mds/penguins.md", "r")
    md_content = md.read()
    md.close()

    blocks = split_blocks(md_content)

    for block in blocks:
        print(block)

    markdown_to_html_node(blocks)




















def markdown_to_html_node(blocks):


    root = ParentNode("div")


    for block in blocks:
        node = markdown_block_to_html_nodes(block)
        root.add_child(node)

        
    print(root.to_html())