from gencontent import reset_public, generate_pages_recursive


def main():
    reset_public()
    generate_pages_recursive("content/", "template.html", "public/")


if __name__ == "__main__":
    main()