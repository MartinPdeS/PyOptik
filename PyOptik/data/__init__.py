from PyOptik.data.default import default_material

def build_default_library() -> None:
    """
    Downloads and saves the default materials from the specified URLs.
    """
    from PyOptik.utils import download_yml_file

    for name, url in default_material.items():
        download_yml_file(url=url, filename=name)


if __name__ == '__main__':
    build_default_library()