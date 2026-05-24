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
                         
