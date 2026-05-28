def markdown_to_blocks(markdown:str)->list[str]:
    blocks = []
    result = []
    blocks.extend(markdown.split("\n\n"))
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block != "":
            result.append(stripped_block)
    return result
    
