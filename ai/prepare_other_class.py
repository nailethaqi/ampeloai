from pathlib import Path
import random
import shutil
import re

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SOURCE_DIR = (
    Path.home()
    / "Downloads"
    / "PlantVillage-Dataset-master"
    / "PlantVillage-Dataset-master"
    / "raw"
    / "color"
)

OTHER_DIR = PROJECT_ROOT / "dataset" / "source" / "Other"

PLANTS = {
    "Apple": 125,
    "Tomato": 125,
    "Potato": 125,
    "Pepper": 125,
    "Peach": 125,
    "Corn": 125,
    "Strawberry": 125,
    "Cherry": 125,
}

SEED = 42

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png"
}


def normalize_name(name):
    return re.sub(r"[^a-zA-Z0-9]+", "_", name).strip("_")


def find_plant_images(plant_name):
    images = []

    for folder in SOURCE_DIR.iterdir():
        if not folder.is_dir():
            continue

        folder_name = folder.name.lower()
        plant_lower = plant_name.lower()

        if plant_lower in folder_name and "grape" not in folder_name:
            for file in folder.iterdir():
                if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS:
                    images.append(file)

    return images


def main():
    random.seed(SEED)

    if not SOURCE_DIR.exists():
        print("ERROR: PlantVillage color folder was not found:")
        print(SOURCE_DIR)
        return

    OTHER_DIR.mkdir(parents=True, exist_ok=True)

    for old_file in OTHER_DIR.iterdir():
        if old_file.is_file():
            old_file.unlink()

    total_copied = 0

    for plant_name, amount in PLANTS.items():
        images = find_plant_images(plant_name)

        print(f"{plant_name}: {len(images)} images found")

        if len(images) < amount:
            print(
                f"WARNING: Only {len(images)} images available for {plant_name}."
            )
            selected = images
        else:
            selected = random.sample(images, amount)

        for index, source_file in enumerate(selected, start=1):
            source_folder = normalize_name(source_file.parent.name)

            destination_name = (
                f"{normalize_name(plant_name)}_"
                f"{source_folder}_"
                f"{index:04d}"
                f"{source_file.suffix.lower()}"
            )

            destination = OTHER_DIR / destination_name

            shutil.copy2(source_file, destination)
            total_copied += 1

        print(f"Copied: {len(selected)}")

    print()
    print("--------------------------------")
    print(f"Total images copied: {total_copied}")
    print(f"Destination: {OTHER_DIR}")
    print("--------------------------------")


if __name__ == "__main__":
    main()