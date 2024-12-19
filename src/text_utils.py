from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ORDERED_LIST = "ordered_list"
    UNORDERED_LIST = "unordered_list"


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
        return BlockType.HEADING
    
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


# def block_to_block_type(block: str) -> BlockType:
#     match block[0]:
#         # Headings start with 1-6 # characters, followed by a space and then the heading text.
#         case '#':
#             heading = block.split(maxsplit=1)[0]
#             if set(heading) != set('#') or len(heading) > 6:
#                 raise ValueError(f"too many #, {len(heading)} provided" if set(heading) == set('#')
#                                  else f"expecting only #, instead found {set(heading) - set('#')}")
#             return BlockType.HEADING
#         # Code blocks must start with 3 backticks and end with 3 backticks.
#         case '`':
#             code = block.split("```")
#             if len(code) % 2 != 1 or len(code) < 3:
#                 raise ValueError("missing closing code delimiters")
#             return BlockType.CODE
#         # Every line in a quote block must start with a > character.
#         case '>':
#             quotes = block.split('\n')
#             for quote in quotes:
#                 if quote.strip()[0] != '>':
#                     raise ValueError("missing > character from start of line in quote block")
#             return BlockType.QUOTE
#         # Every line in an unordered list block must start with a * or - character, followed by a space.
#         case '*' | '-':
#             u_list = block.split('\n')
#             for item in u_list:
#                 start = item.strip()[:2]
#                 if not (start == "* " or start == "- "):
#                     raise ValueError("unordered list block must start with a * or - character, followed by a space")
#             return BlockType.UNORDERED_LIST
#         # Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
#         case '1':
#             o_list = block.split('\n')
#             for index, item in enumerate(o_list, start=1):
#                 if item.strip()[:3] != f"{index}. ":
#                     raise ValueError("ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line")
#             return BlockType.ORDERED_LIST
#         # If none of the above conditions are met, the block is a normal paragraph.
#         case _:
#             return BlockType.PARAGRAPH
        