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