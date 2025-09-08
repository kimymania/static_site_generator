import os
import shutil
import sys

from generate_page import generate_pages_recursive


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    cwd = os.getcwd()
    docs_folder = os.path.join(cwd, "docs")
    static_folder = os.path.join(cwd, "static")

    # Delete contents of public folder
    if not os.path.exists(docs_folder):
        os.mkdir(docs_folder)
    elif len(os.listdir(docs_folder)) > 0:
        delete_contents(docs_folder)

    # Copy contents of static folder to public folder
    copy_contents(static_folder, docs_folder)

    # Generate page from content/index.md using template.html and write it to public/index.html
    md_path = os.path.join(cwd, "content")
    template_path = os.path.join(cwd, "template.html")
    generate_pages_recursive(md_path, template_path, docs_folder, basepath)


def delete_contents(path):
    """Delete public folder -> Create new empty public folder"""
    shutil.rmtree(path)
    os.mkdir(path)


def copy_contents(path, target):
    """Copy all files, nested files and subdirectories from static folder to public folder"""
    # shutil.copytree(static, public)
    files = os.listdir(path)
    for file in files:
        filepath = os.path.join(path, file)
        if os.path.isdir(filepath):
            new_target = os.path.join(target, file)
            os.mkdir(new_target)
            copy_contents(filepath, new_target)
        else:
            shutil.copy(filepath, target)


main()
