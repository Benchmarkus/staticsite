import os
import shutil
import re
from conversion import markdown_to_blocks, block_to_block_type, markdown_to_html_node
from blocktype import BlockType

def main():
    clear_source("public")
    copy_from_directory_to("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

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

def extract_title(markdown):
    listOfBlock = markdown_to_blocks(markdown)
    for block in listOfBlock:
        if block_to_block_type(block) == BlockType.HEADING:
            if re.match(r"^#{1} ", block) != None:
                return block.replace("# ", "").strip()
    raise Exception("no header #1")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown_file = f.read()

    with open(template_path, "r") as f:
        template_file = f.read()

    html_string = markdown_to_html_node(markdown_file).to_html()
    title_string = extract_title(markdown_file)

    template_file_titled_contented = template_file.replace(r"{{ Title }}", title_string)
    template_file_titled_contented = template_file_titled_contented.replace(r"{{ Content }}", html_string)


    with open(dest_path, "w") as f:
        f.write(template_file_titled_contented)

main()

