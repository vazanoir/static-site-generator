from shutil import rmtree
from os import mkdir


def main():
    public = "public"
    rmtree(public)
    mkdir(public)


if __name__ == "__main__":
    main()
