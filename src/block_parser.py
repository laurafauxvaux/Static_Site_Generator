from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_parser import text_to_textnodes
    
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown:str)->list[str]:
    blocks = []
    result = []
    blocks.extend(markdown.split("\n\n"))
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block != "":
            result.append(stripped_block)
    return result

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
            and any(section[1:].strip() != "" for section in sections)
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

def _text_to_children(text:str) ->list[HTMLNode]:
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children

def _heading_to_html_node(text:str)->ParentNode:
    sections = text.split(" ", 1)
    tag_number = len(sections[0])
    value = sections[1]
    children = _text_to_children(value)
    return ParentNode(f"h{tag_number}", children)

def _code_to_html_node(text:str)->ParentNode:
    sections = text.split("```")
    text_node = TextNode(sections[1][1:], TextType.CODE)
    code_node = text_node_to_html_node(text_node)
    return ParentNode("pre", [code_node])

def _quote_to_html_node(text:str)->ParentNode:
    sections = text.split("\n")
    child = "\n".join(section[1:].strip() for section in sections)
    children = _text_to_children(child)
    return ParentNode("blockquote", children)

def _unordered_list_to_html_node(text:str)->ParentNode:
    sections = text.split("\n")
    children = []
    for section in sections:
        grandchildren = _text_to_children(section[1:].strip())
        children.append(ParentNode("li", grandchildren))
    return ParentNode("ul", children)

def _ordered_list_to_html_node(text:str)->ParentNode:
    sections = text.split("\n")
    children = []
    for section in sections:
        number, content = section.split(" ", 1)
        grandchildren = _text_to_children(content.strip())
        children.append(ParentNode("li", grandchildren))
    return ParentNode("ol", children)

def _paragraph_to_html_node(text:str)->ParentNode:
    new_lines = text.replace("\n", " ")
    return ParentNode("p", _text_to_children(new_lines))  

    
def markdown_to_html_node(markdown:str)->ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                node = _heading_to_html_node(block)
            case BlockType.CODE:
                node = _code_to_html_node(block)
            case BlockType.QUOTE:
                node = _quote_to_html_node(block)
            case BlockType.UNORDERED_LIST:
                node = _unordered_list_to_html_node(block)
            case BlockType.ORDERED_LIST:
                node = _ordered_list_to_html_node(block)
            case BlockType.PARAGRAPH:
                node = _paragraph_to_html_node(block)
        children.append(node)
    
    parent_node = ParentNode("div", children)
    return parent_node
            

    



