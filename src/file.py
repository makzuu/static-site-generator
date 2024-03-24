import os
import shutil

def delete_if_exists(dir):
    if os.path.exists(dir):
        print(f"removing directory {dir}...")
        shutil.rmtree(dir)

def copy_tree(src, dest):
    if not os.path.exists(dest):
        print(f"creating directory {dest}...")
        os.mkdir(dest)
    for file in os.listdir(src):
        file_path = os.path.join(src, file)
        dest_path = os.path.join(dest, file)
        if os.path.isfile(file_path):
            print(f"copying {file_path} to {dest_path}...")
            shutil.copy(file_path, dest_path)
        else:
            copy_tree(file_path, dest_path)
