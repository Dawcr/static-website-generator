from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    CODE = "code"
    QUOTE = "quote"
    ORDERED_LIST = "ordered_list"
    UNORDERED_LIST = "unordered_list"
    HEADING1 = "heading 1"
    HEADING2 = "heading 2"
    HEADING3 = "heading 3"
    HEADING4 = "heading 4"
    HEADING5 = "heading 5"
    HEADING6 = "heading 6"

def markdown_to_blocks(markdown: str) -> list[str]:
    lines = markdown.split('\n')
    blocks: list[str] = []
    
    block: list[str] = []
    for line in lines:
        if not line.strip():
            if block:
                blocks.append('\n'.join(block))
                block = []
            continue
        
        block.append(line.strip())
        
    if block:
        blocks.append('\n'.join(block))
        
    return blocks


def block_to_block_type(block: str) -> BlockType:
    lines = block.split('\n')
    
    # Headings start with 1-6 # characters, followed by a space and then the heading text.
    if block.startswith(("#", "##", "###", "####", "#####", "######", "#######")):
        start = block.split(maxsplit=1)[0]
        return BlockType(f"heading {len(start)}")
    
    # Code blocks must start with 3 backticks and end with 3 backticks.
    if len(lines) > 1 and block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    # Every line in a quote block must start with a > character.
    if block.startswith('>'):
        for line in lines:
            if not line.startswith('>'):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    # Every line in an unordered list block must start with a * or - character, followed by a space.
    if block.startswith(("* ", "- ")):
        start = block[:2]
        for line in lines:
            if not line.startswith(start):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    # Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
    if block.startswith("1. "):
        for index, line in enumerate(lines, start=1):
            if not line.startswith(f"{index}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    
    # If none of the above conditions are met, the block is a normal paragraph.
    return BlockType.PARAGRAPH


