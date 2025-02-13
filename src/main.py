import os
import shutil
from copy_static import copy_to_destination
from md_blocks import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_to_destination(dir_path_static, dir_path_public)
    generate_pages_recursive("content", "template.html", "public")

main()
