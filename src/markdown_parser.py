import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type:TextType) ->list[TextNode]:
    result = []
    to_check = []

    if not isinstance(delimiter, str) or delimiter == "":
        raise ValueError("Delimiter must be a non-empty string")

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
        else:
            to_check.append(node)

    if not to_check:
        return result
    
    for node in to_check:
        new_nodes = []
        split_text = node.text.split(delimiter)

        if len(split_text) % 2 == 0:
            raise Exception("A delimiter wasn't closed: invalid Markdown syntax")
        for i in range(len(split_text)):
            if i % 2 == 0:
                new_nodes.append(TextNode(split_text[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_text[i], text_type))
        result.extend(new_nodes)

    return result

def extract_markdown_images(text:str) -> list[tuple[str, str]]:          
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text:str) -> list[tuple[str, str]]:          
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes:list[TextNode]) -> list[TextNode]:
    result = []

    for node in old_nodes:
        initial_text = node.text
        extracted_image = []
        extracted_image.extend(extract_markdown_images(node.text))
        
        current_text = initial_text 
        if not extracted_image:
            result.append(TextNode(current_text, TextType.TEXT))
        else:  
            for img in extracted_image:             
                img_alt = img[0]
                img_src = img[1]          
                section = current_text.split(f"![{img_alt}]({img_src})", 1)
                if len(section) < 2 and section[0]:
                    continue
                else:
                    before_img, after_img = section[0], section[1]
                    
                    if before_img != "":
                        result.append(TextNode(before_img, TextType.TEXT))
                    result.append(TextNode(img_alt, TextType.IMAGE, img_src))
                    current_text = after_img

            if current_text != "":
                result.append(TextNode(current_text, TextType.TEXT))

    return result

def split_nodes_link(old_nodes:list[TextNode]) -> list[TextNode]:
    result = []

    for node in old_nodes:
        initial_text = node.text
        extracted_links = []
        extracted_links.extend(extract_markdown_links(node.text))
        
        current_text = initial_text 
        if not extracted_links:
            result.append(TextNode(current_text, TextType.TEXT))
        else:  
            for link in extracted_links:             
                href = link[0]
                url = link[1]          
                section = current_text.split(f"[{href}]({url})", 1)
                if len(section) < 2 and section[0]:
                    continue
                else:
                    before_link, after_link = section[0], section[1]
                    
                    if before_link != "":
                        result.append(TextNode(before_link, TextType.TEXT))
                    result.append(TextNode(href, TextType.LINK, url))
                    current_text = after_link

            if current_text != "":
                result.append(TextNode(current_text, TextType.TEXT))

    return result