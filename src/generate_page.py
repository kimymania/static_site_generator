import os

from markdown_blocks import extract_title, markdown_to_html_node


def generate_page(from_path, template_path, dest_path) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    lines = []
    with open(from_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            lines.append(line)
    md_content = "".join(lines)

    lines = []
    with open(template_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            lines.append(line)
    template_content = "".join(lines)

    html_node = markdown_to_html_node(md_content)
    html_content = html_node.to_html()
    html_title = extract_title(md_content)

    new_html = template_content.replace("{{ Title }}", html_title)
    new_html = new_html.replace("{{ Content }}", html_content)

    dir = os.path.dirname(dest_path)

    if not os.path.exists(dir):
        os.makedirs(dir)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(new_html)
