import os
import shutil

def copy_to_destination(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    
    for file in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, file)
        dest_path = os.path.join(dest_dir_path, file)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_to_destination(from_path, dest_path)