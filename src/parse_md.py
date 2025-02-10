from enum import Enum
from src.html_node import *
from src.text_to_text_nodes import *
from src.md_block import *
from src.md_blocks_to_html_nodes import *


def identify_block_type(line):

    line = line.lstrip()
    if (
        line == ""
    ):  # This condition is true only when the function is called by the while loop condition of code_block_helper, so it's fine to return PARAGRAPH
        return BlockType.PARAGRAPH

    if line.startswith("#"):
        return BlockType.HEADING
    if line.startswith("- ") or line.startswith("* "):
        return BlockType.UNORDERED_LIST
    if line[0] in "0123456789" and "." in line[0:3]:
        return BlockType.ORDERED_LIST
    if line.startswith("```") or line.startswith("~~~"):
        return BlockType.CODE
    if line.startswith(">"):
        return BlockType.QUOTE
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
    while index < len(lines) and identify_block_type(lines[index]) != BlockType.CODE:
        content.append(lines[index])
        index += 1

    return MarkdownBlock(BlockType.CODE, content), index + 1  # exclude the ending ```


def quote_block_helper(lines, index):
    content = []
    content.append(lines[index])
    index += 1
    while (
        index < len(lines)
        and lines[index].strip() != ""
        and identify_block_type(lines[index]) in [BlockType.PARAGRAPH, BlockType.QUOTE]
    ):
        content.append(lines[index])
        index += 1

    return MarkdownBlock(BlockType.QUOTE, content), index


def list_block_helper(lines, index, spaces, n_of_spaces, block_type):

    content = []
    content.append(lines[index])
    index += 1
    # required space to be considered inside the current section
    space_required = spaces * n_of_spaces

    while index < len(lines) and (
        lines[index].startswith(
            space_required
        )  # we should not jump to parent section when child section ends
        and (
            identify_block_type(lines[index]) == block_type
            or lines[index].startswith(space_required + spaces)
        )
        or lines[index] == ""
    ):

        if lines[index] == "":  # if line is empty
            index += 1
        elif lines[index].startswith(
            spaces * (n_of_spaces) + 2 * SPACE
        ):  # if line is the beginning of subsection
            # identify how many space characters make up one tab
            if n_of_spaces == 0:
                spaces = SPACE * (len(lines[index]) - len(lines[index].lstrip()))
                child_block, index = retrieve_block(lines, index, spaces, 1)
            else:
                child_block, index = retrieve_block(
                    lines, index, spaces, n_of_spaces + 1
                )
            content.append(child_block)

        else:  # if line is a list item
            content.append(lines[index])
            index += 1

    return MarkdownBlock(block_type, content), index


def retrieve_block(lines, index, spaces, n_of_spaces):

    # if there is too much indentation, line is considered as paragraph
    if lines[index].startswith(spaces * (n_of_spaces + 2)):
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
            block, index = list_block_helper(
                lines, index, spaces, n_of_spaces, block_type
            )

        case BlockType.UNORDERED_LIST:
            block, index = list_block_helper(
                lines, index, spaces, n_of_spaces, block_type
            )

        case BlockType.CODE:
            block, index = code_block_helper(lines, index)

        case BlockType.QUOTE:
            block, index = quote_block_helper(lines, index)

    return block, index


# `spaces` is used for LIST type to parse child sections
def split_blocks(markdown):

    blocks = []
    lines = markdown.split("\n")
    index = 0

    while index < len(lines):
        # markdown ignores whitespace between text
        if lines[index].strip() == "":
            index += 1
            continue
        block, index = retrieve_block(lines, index, SPACE * 2, 0)

        #        index += 1
        blocks.append(block)

    return blocks


def md_to_html(markdown):
    md_blocks = split_blocks(markdown)

    html_node = md_to_html_node(md_blocks)

    return html_node.to_html()
