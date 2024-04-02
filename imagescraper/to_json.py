import json
from pathlib import Path

from .config import IMG_OUTPUT_DIR


FolderData = dict[str, str | list[str]]
Folders = list[FolderData]

# TODO get the path of the script and the dir
# and strip that out so the path starts with /var for each image


def read_metadata(metadata_file: Path) -> tuple[str, str]:
    """
    Reads metadata from a given metadata file.

    :param metadata_file: Path to the metadata file.

    :returns: A tuple containing the URL and description.
    """
    with open(metadata_file, "r", encoding="utf-8") as metadata:
        url = metadata.readline().strip()
        description = metadata.readline().strip()

    return url, description


def generate_folder_data(parent_folder: Path) -> Folders:
    """
    Get info on prompts and images for each folder in a given folder.
    """
    folders = []

    for folder in parent_folder.iterdir():
        if not folder.is_dir():
            continue

        metadata_file = folder / "metadata.txt"

        if not metadata_file.exists():
            continue

        url, description = read_metadata(metadata_file)
        image_paths = folder.glob("*.png")
        image_files = [str(path) for path in image_paths]

        folder_data: FolderData = {
            "folderName": folder.name,
            "url": url,
            "description": description,
            "images": image_files,
        }

        folders.append(folder_data)

    return folders


def write_json(data: Folders, output_file: Path):
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=2)


def main():
    parent_folder_path = IMG_OUTPUT_DIR
    output_json_path = Path("output.json")

    data_to_write = generate_folder_data(parent_folder_path)
    write_json(data_to_write, output_json_path)


if __name__ == "__main__":
    main()
