from pathlib import Path
import shutil

import kagglehub


DATASET = "jessicali9530/stanford-dogs-dataset"
IMAGES_PER_BREED = 10
OUTPUT_DIR = Path("images") / "stanford_dogs_subset"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def breed_name(folder_name):
    if "-" in folder_name:
        folder_name = folder_name.split("-", 1)[1]
    return folder_name.lower().replace(" ", "_")


def find_breed_folders(dataset_path):
    folders = []

    for folder in Path(dataset_path).rglob("*"):
        if not folder.is_dir():
            continue

        images = [
            image
            for image in folder.iterdir()
            if image.is_file() and image.suffix.lower() in IMAGE_EXTENSIONS
        ]

        if images:
            folders.append((folder, sorted(images)))

    return sorted(folders, key=lambda item: item[0].name.lower())


def main():
    dataset_path = kagglehub.dataset_download(DATASET)
    print("Path to dataset files:", dataset_path)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    copied = 0
    breed_folders = find_breed_folders(dataset_path)

    for folder, images in breed_folders:
        breed = breed_name(folder.name)

        for index, image in enumerate(images[:IMAGES_PER_BREED], start=1):
            output_name = f"{breed}_{index:02d}{image.suffix.lower()}"
            shutil.copy2(image, OUTPUT_DIR / output_name)
            copied += 1

    print(f"Copied {copied} images into: {OUTPUT_DIR.resolve()}")
    print(f"Breeds found: {len(breed_folders)}")


if __name__ == "__main__":
    main()

