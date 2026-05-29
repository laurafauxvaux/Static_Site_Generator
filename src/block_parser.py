from enum import Enum

def markdown_to_blocks(markdown:str)->list[str]:
    blocks = []
    result = []
    blocks.extend(markdown.split("\n\n"))
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block != "":
            result.append(stripped_block)
    return result
    
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown_text:str)->BlockType:
    if markdown_text.startswith("#"):
        sections = markdown_text.split(" ", 1)
        if (
            len(sections) == 2
            and sections[1] != ""
            and all(char == "#" for char in sections[0])
            and 0 < len(sections[0]) < 7
        ):
            return BlockType.HEADING
        return BlockType.PARAGRAPH
        
    elif markdown_text.startswith("```\n") and markdown_text.endswith("```"):
        return BlockType.CODE
    
    elif markdown_text.startswith(">"):
        sections = markdown_text.split("\n")
        if (
            all(section.startswith(">") for section in sections)
            and all(section[1:].strip() != "" for section in sections)
        ):
            return BlockType.QUOTE
        return BlockType.PARAGRAPH
        
    elif markdown_text.startswith("- "):
        sections = markdown_text.split("\n")
        if all(section.startswith("- ") for section in sections):
            return BlockType.UNORDERED_LIST
        return BlockType.PARAGRAPH
            
    elif markdown_text.startswith("1. "):
        sections = markdown_text.split("\n")
        number = 1
        for section in sections:
            if section.startswith(f"{number}. "):
                number += 1
            else:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    
    else:
        return BlockType.PARAGRAPH