"""
To JSON module.

Build a JSON file of data based on the images and metadata text files
stored in creations. This can be used for a web app for browsing content.
"""

import json
from pathlib import Path
from typing import Optional

from .config import IMG_OUTPUT_DIR, WEB_APP_DATA, VAR_DIR


FolderData = dict[str, str | list[str]]
Folders = list[FolderData]


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


def get_image_files(folder: Path, base_path: Path) -> list[str]:
    """
    Get a list of image files in a given folder.

    :param folder: Path to the folder containing images.
    param base_path: This is used as the base, so the part on the left is removed.

    :returns: List of image paths.
    """
    image_paths = folder.glob("*.png")
    return [str(path.relative_to(base_path)) for path in image_paths]


def get_folder_data(folder: Path) -> Optional[FolderData]:
    """
    Get info about a given creation folder.
    """
    if not folder.is_dir():
        return None

    metadata_file = folder / "metadata.txt"

    if not metadata_file.exists():
        return None

    url, description = read_metadata(metadata_file)
    image_files = get_image_files(folder, VAR_DIR)

    folder_data: FolderData = {
        "folderName": folder.name,
        "url": url,
        "description": description,
        "images": image_files,
    }

    return folder_data


def generate_folder_data(parent_folder: Path) -> Folders:
    """
    Get info on prompts and images for each folder in a given folder.
    """
    folders_data = [get_folder_data(folder) for folder in parent_folder.iterdir()]

    return [f for f in folders_data if f]


def write_json(data: list[dict], output_file: Path) -> None:
    """
    Write out given data as a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=2)


def main() -> None:
    """
    Main command-line entry-point.
    """
    parent_folder_path = IMG_OUTPUT_DIR
    output_json_path = WEB_APP_DATA

    data_to_write = generate_folder_data(parent_folder_path)

    print(f"Writing to: {output_json_path}")
    write_json(data_to_write, output_json_path)


if __name__ == "__main__":
    main()
