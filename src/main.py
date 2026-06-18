import os
import shutil
from htmlnode import HTMLNode
from page_generator import generate_page
from block_parser import block_to_block_type
        

def copy_static_to_public(static_path:str, public_path:str):
    if os.path.exists(static_path):
        current_path = static_path
        for item in os.listdir(static_path):
            complete_path = os.path.join(current_path, item)
            if os.path.isdir(complete_path):
                dst_child = os.path.join(public_path, item)
                os.mkdir(dst_child)
                copy_static_to_public(complete_path, dst_child)
            elif os.path.isfile(complete_path):
                shutil.copy(complete_path, public_path)
                print(complete_path)



def main():
    if os.path.exists('./public'):
        shutil.rmtree('./public')
    os.mkdir('./public')
    copy_static_to_public('./static', './public')
    generate_page('./content/index.md', './template.html', './public/index.html')


if __name__ == "__main__":
    main()