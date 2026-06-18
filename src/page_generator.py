import os
from block_parser import (BlockType,
                          block_to_block_type,
                          markdown_to_blocks, 
                          markdown_to_html_node)


def extract_title(markdown:str)->str:
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
       if block_to_block_type(block) == BlockType.HEADING:
           if block.startswith("# "):
               return block[2:].strip()
           
    raise Exception("No header in this markdown file")


def generate_page(from_path:str, template_path:str, dest_path:str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        index_contents = f.read()

    with open(template_path, "r") as f:
        template_contents = f.read()

    from_doc_html_nodes = markdown_to_html_node(index_contents)
    from_doc_html_str = from_doc_html_nodes.to_html()

    title = extract_title(index_contents)

    with_title = template_contents.replace("{{ Title }}", f"{title}")
    final_html = with_title.replace("{{ Content }}", f"{from_doc_html_str}")

    target_directory = os.path.dirname(dest_path)
    os.makedirs(target_directory, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(final_html)
        
