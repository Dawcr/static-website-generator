import os
import shutil
import sys

from textnode import *
from htmlnode import *
from node_utils import *
from text_utils import *


def main():
    reset_public()
    generate_page("content/index.md", "template.html", "public/")


def reset_public() -> None:
    cwd = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.dirname(cwd)
    public_dir = os.path.join(root_dir, "public")
    static_dir = os.path.join(root_dir, "static")
    
    if os.path.exists(public_dir):
        print(f"deleting {public_dir}")
        shutil.rmtree(public_dir)
        
    os.mkdir(public_dir)
        
    if not os.path.exists(static_dir):
        print(f"{static_dir} missing, nothing to copy")
        return
    
    # we hate shutil.copytree() in this course
    def copy_contents(path = "") -> None:
        static_path = os.path.join(static_dir, path)
        with os.scandir(static_path) as it:
            for pt in it:
                public_path = os.path.join(public_dir, path)
                if pt.is_dir():
                    print(f"creating {pt.name} directory in {os.path.relpath(public_path, start=root_dir)}")
                    relative_path = os.path.relpath(pt, start=static_dir)
                    new_dir = os.path.join(public_path, pt.name)
                    os.mkdir(new_dir)
                    copy_contents(relative_path)
                    continue
                if pt.is_file():
                    print(f"copying {pt.name} to {os.path.relpath(public_path, start=root_dir)}")
                    shutil.copy(pt, public_path)
                
    copy_contents()


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = get_file_content(from_path)
    template = get_file_content(template_path)
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    file_name, _ = os.path.splitext(os.path.basename(from_path))
    file_name += ".html"
    new_file_path = os.path.join(dest_path, file_name)
    
    if not os.path.exists(dest_path):
        cwd = os.path.dirname(os.path.realpath(__file__))
        root_dir = os.path.dirname(cwd)
        additional_dirs = os.path.relpath(os.path.abspath(dest_path), root_dir)
        
        def create_path(path: str) -> None:
            parent_dir = os.path.dirname(path)
            if not os.path.exists(parent_dir):
                create_path(parent_dir)
                
            print(f"Creating {path}")
            os.mkdir(path)
            
        create_path(dest_path)
        
    with open(new_file_path, "w+") as file:
        print(f"writing to {new_file_path}")
        file.write(full_html)



if __name__ == "__main__":
    main()