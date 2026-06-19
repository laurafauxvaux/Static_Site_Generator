import os
from pathlib import Path
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


def generate_page(from_path:str, template_path:str, dest_path:str, basepath:str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        index_contents = f.read()

    with open(template_path, "r") as f:
        template_contents = f.read()

    from_doc_html_nodes = markdown_to_html_node(index_contents)
    from_doc_html_str = from_doc_html_nodes.to_html()

    title = extract_title(index_contents)

    with_title = template_contents.replace("{{ Title }}", f"{title}")
    change_contents = with_title.replace("{{ Content }}", f"{from_doc_html_str}")
    href_change = change_contents.replace('href="/', f'href="{basepath}')
    final_html = href_change.replace('src="/', f'src="{basepath}')

    target_directory = os.path.dirname(dest_path)
    os.makedirs(target_directory, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content:str, template_path:str, dest_dir_path:str, basepath:str):
    if os.path.exists(dir_path_content):
        for item in os.listdir(dir_path_content):
            complete_path = os.path.join(dir_path_content, item)
            if os.path.isdir(complete_path):
                dst_child = os.path.join(dest_dir_path, item)
                os.mkdir(dst_child)
                generate_pages_recursive(complete_path, template_path, dst_child)
            elif os.path.isfile(complete_path):
                p = Path(complete_path)
                if p.suffix == ".md":
                    html_item = p.stem + ".html"
                    dest_path = os.path.join(dest_dir_path, html_item)
                    generate_page(complete_path, template_path, dest_path)


        
