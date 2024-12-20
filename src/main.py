import os
import shutil

from textnode import *
from htmlnode import *
from node_utils import *


def main():
    reset_public()


def reset_public() -> None:
    cwd = os.path.dirname(os.path.realpath(__file__))
    root_dir, _ = os.path.split(cwd)
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


if __name__ == "__main__":
    main()