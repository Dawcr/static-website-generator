import os
import shutil

from text_utils import (
    get_file_content,
    extract_title
)
from node_utils import markdown_to_html_node


def main():
    reset_public()
    generate_pages_recursive("content/", "template.html", "public/")


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
                if pt.is_file():
                    print(f"copying {pt.name} to {os.path.relpath(public_path, start=root_dir)}")
                    shutil.copy(pt, public_path)
                
    copy_contents()


def generate_page(from_path: os.DirEntry, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path.name} to {dest_path} using {template_path}")
    markdown = get_file_content(from_path)
    template = get_file_content(template_path)
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    file_name, _ = os.path.splitext(os.path.basename(from_path))
    file_name += ".html"
    new_file_path = os.path.join(dest_path, file_name)
    
    if not os.path.exists(dest_path):
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


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    cwd = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.dirname(cwd)
    public_dir_path = os.path.relpath(os.path.abspath(dest_dir_path), start=root_dir)
    public_dir = os.path.join(root_dir, public_dir_path)
    content_dir_path = os.path.relpath(os.path.abspath(dir_path_content), start=root_dir)
    content_dir = os.path.join(root_dir, content_dir_path)
    template_dir_path = os.path.relpath(os.path.abspath(template_path), start=root_dir)
    template_dir = os.path.join(root_dir, template_dir_path)
    
    def generate(content_path: str) -> None:
        with os.scandir(content_path) as it:
            for pt in it:
                if pt.is_file():
                    dest_dir = os.path.join(public_dir, os.path.relpath(os.path.dirname(pt.path), start=content_dir))
                    _, extension = os.path.splitext(pt)
                    print(extension)
                    if extension == ".md":
                        generate_page(pt, template_dir, dest_dir)
                if pt.is_dir():
                    generate(pt)
                    
    generate(content_dir)


if __name__ == "__main__":
    main()