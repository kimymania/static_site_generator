import os
import shutil

from generate_page import generate_pages_recursive


def main():
    cwd = os.getcwd()
    public_folder = os.path.abspath(os.path.join(cwd, "public"))
    static_folder = os.path.abspath(os.path.join(cwd, "static"))

    # Delete contents of public folder
    if not os.path.exists(public_folder):
        os.mkdir(public_folder)
    elif len(os.listdir(public_folder)) > 0:
        delete_contents(public_folder)

    # Copy contents of static folder to public folder
    copy_contents(static_folder, public_folder)

    # Generate page from content/index.md using template.html and write it to public/index.html
    md_path = os.path.join(cwd, "content")
    template_path = os.path.join(cwd, "template.html")
    dest_path = os.path.join(cwd, "public")
    generate_pages_recursive(md_path, template_path, dest_path)


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
