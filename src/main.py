import os
import shutil

def main():
    clear_source("public")
    copy_from_directory_to("static", "public")

def clear_source(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
        os.mkdir(directory)

def copy_from_directory_to(source, destination):
    os.makedirs(destination, exist_ok=True)
    for item in os.listdir(source):
        s = os.path.join(source, item)
        d = os.path.join(destination, item)
        if os.path.isdir(s):
            copy_from_directory_to(s, d)
        else:
            shutil.copy(s, d)

main()