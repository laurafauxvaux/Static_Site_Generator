import os
import shutil
import sys
from page_generator import generate_pages_recursive

        

def copy_static_to_public(static_path:str, public_path:str):
    if os.path.exists(static_path):
        for item in os.listdir(static_path):
            complete_path = os.path.join(static_path, item)
            if os.path.isdir(complete_path):
                dst_child = os.path.join(public_path, item)
                os.mkdir(dst_child)
                copy_static_to_public(complete_path, dst_child)
            elif os.path.isfile(complete_path):
                shutil.copy(complete_path, public_path)
                print(complete_path)



def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    if os.path.exists('./docs'):
        shutil.rmtree('./docs')
    os.mkdir('./docs')
    copy_static_to_public('./static', './docs')
    generate_pages_recursive('./content', './template.html', './docs', basepath)
    
    


if __name__ == "__main__":
    main()