import re
from conversion import markdown_to_html_node
from os import makedirs, path, mkdir, listdir


def extract_title(markdown):
    title = re.search(r"^# .+", markdown)

    if title is None:
        raise Exception("page need a title")

    return title[0][2:]


def generate_page(source_path, template_path, dest_path):
    print(
        f"Generating page from {source_path} to "
        f"{dest_path} using {template_path}"
    )

    source_file = open(source_path)
    source_buffer = source_file.read()

    template_file = open(template_path)
    template_buffer = template_file.read()

    title = extract_title(source_buffer)
    source_as_html = markdown_to_html_node(source_buffer).to_html()

    template_buffer = template_buffer.replace("{{ Title }}", title)
    template_buffer = template_buffer.replace("{{ Content }}", source_as_html)

    makedirs(path.dirname(dest_path), exist_ok=True)

    dest_file = open(dest_path, mode='w')
    dest_file.write(template_buffer)


def generate_pages_recursive(source_path, template_path, dest_path):
    ls = listdir(source_path)

    for item in ls:
        source_item = path.join(source_path, item)
        dest_item = path.join(dest_path, item)

        if path.isfile(source_item):
            generate_page(
                source_item,
                template_path,
                dest_item.replace("md", "html")
            )
        else:
            mkdir(dest_item)
            generate_pages_recursive(source_item, template_path, dest_item)
