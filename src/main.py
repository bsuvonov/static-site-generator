from src.text_node import *
from src.html_node import *
from src.text_to_text_nodes import *
from src.parse_md import *
import os
import shutil


def recursive_delete(src):
    content = os.listdir(src)
    for item in content:
        target = os.path.join(src, item)
        if os.path.isfile(target):
            os.remove(target)
        else:
            recursive_delete(target)
            os.rmdir(target)


def recursive_copy(src, dest):
    content = os.listdir(src)
    for item in content:
        src_item = os.path.join(src, item)
        dest_item = os.path.join(dest, item)

        if os.path.isfile(src_item):
            shutil.copy(src_item, dest_item)
        else:
            os.mkdir(dest_item)
            recursive_copy(src_item, dest_item)


# prepares new `public` folder for output
def prepare_public():
    src = "./static"
    dest = "./public"

    # recursively delete dest folder if it exists
    if os.path.exists(dest):
        recursive_delete(dest)
        os.rmdir(dest)

    # recursively copy src to dest
    os.mkdir("./public")
    if os.path.exists("./static"):
        recursive_copy(src, dest)
    else:
        raise Exception("Folder `static` doesn't exist")


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.lstrip().startswith("# "):
            return line.strip()[2:]

    raise Exception("Markdown has no title (no `h1` header found)")


def write_page(dest, template, title, html):
    for line in template:
        if r"{{ Title }}" in line:
            line = line.replace(r"{{ Title }}", title)
        elif r"{{ Content }}":
            line = line.replace(r"{{ Content }}", html)
        dest.write(line)


def generate_page(src_path, dest_path, template_path):
    print(f"Generating page from {src_path} to {dest_path} using {template_path}")

    # file opening
    md = open(src_path, "r")
    template = open(template_path, "r")
    dest = open(dest_path, "w")

    # html generation and result output
    md_content = md.read()
    title = extract_title(md_content)
    html = md_to_html(md_content)
    write_page(dest, template, title, html)

    # closing opened files
    md.close()
    dest.close()
    template.close()


def generate_pages_recursive(src_path, dest_path, template_path):
    content = os.listdir(src_path)
    for item in content:
        src_item = os.path.join(src_path, item)
        dest_item = os.path.join(dest_path, item)

        if os.path.isfile(src_item) and src_item[-3:] == ".md":
            generate_page(src_item, dest_item[:-3] + ".html", template_path)
        else:
            if not os.path.exists(dest_item):
                os.mkdir(dest_item)
            generate_pages_recursive(src_item, dest_item, template_path)


def main():
    prepare_public()
    generate_pages_recursive("./content", "./public/", "./template.html")

    return 0


if __name__ == "__main__":
    main()
