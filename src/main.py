from file import delete_if_exists, copy_tree

def main():
    src_path = "static"
    dest_path = "public"
    delete_if_exists(dest_path)
    copy_tree(src_path, dest_path)

main()
