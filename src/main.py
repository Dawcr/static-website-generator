import sys

from gencontent import reset_public, generate_pages_recursive


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    reset_public()
    generate_pages_recursive("content/", "template.html", "docs/", basepath)


if __name__ == "__main__":
    main()