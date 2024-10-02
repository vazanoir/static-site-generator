from shutil import rmtree, copy
from os import mkdir, listdir, path
from pagegen import generate_page


def main():
    remove_dir_content("public")
    copy_tree("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


def copy_tree(source, destination):
    ls = listdir(source)

    for item in ls:
        source_item = path.join(source, item)
        destination_item = path.join(destination, item)

        if path.isfile(source_item):
            copy(source_item, destination_item)
        else:
            mkdir(destination_item)
            copy_tree(source_item, destination_item)


def remove_dir_content(dir):
    rmtree(dir)
    mkdir(dir)


if __name__ == "__main__":
    main()
