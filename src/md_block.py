from enum import Enum

class BlockType(Enum):
    HEADING = "BlockType.HEADING"
    ORDERED_LIST = "BlockType.ORDERED_LIST"
    UNORDERED_LIST = "BlockType.UNORDERED_LIST"
    QUOTE = "BlockType.QUOTE"
    CODE = "BlockType.CODE"
    PARAGRAPH = "BlockType.PARAGRAPH"

SPACE = " "


class MarkdownBlock:
    def __init__(self, type, content):
        self.type = type
        self.content = content

    def __repr__(self):
        repr = f"MarkdownBlock(type={self.type}, content:"
        for elem in self.content:
            repr += f'\n\t{elem}' 
        repr += '\n)'
        return repr 