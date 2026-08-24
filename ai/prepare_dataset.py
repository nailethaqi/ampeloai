from pathlib import Path
import random
import shutil



RANDOM_SEED = 42


TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.15
TEST_RATIO = 0.15



PROJECT_ROOT = Path(__file__).resolve().parent.parent

SOURCE_DIR = PROJECT_ROOT / "dataset" / "source"
TRAIN_DIR = PROJECT_ROOT / "dataset" / "train"
VALIDATION_DIR = PROJECT_ROOT / "dataset" / "validation"
TEST_DIR = PROJECT_ROOT / "dataset" / "test"



CLASSES = {
    "Grape___Black_rot": "Black_Rot",
    "Grape___Esca_(Black_Measles)": "Esca",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": "Leaf_Blight",
    "Grape___healthy": "Healthy",
    "Other": "Other",
}


def get_images(folder):
    """Return all supported image files from a folder."""
    supported_extensions = {".jpg", ".jpeg", ".png"}

    return [
        file
        for file in folder.iterdir()
        if file.is_file() and file.suffix.lower() in supported_extensions
    ]


def prepare_destination_folder(folder):
    """
    Remove an existing class folder and recreate it.
    This prevents duplicate files when the script is run again.
    """
    if folder.exists():
        shutil.rmtree(folder)

    folder.mkdir(parents=True, exist_ok=True)


def split_dataset():
    random_generator = random.Random(RANDOM_SEED)

    print("\nPreparing grape leaf dataset...\n")

    total_train = 0
    total_validation = 0
    total_test = 0

    for source_class, output_class in CLASSES.items():

        source_folder = SOURCE_DIR / source_class

        if not source_folder.exists():
            raise FileNotFoundError(
                f"Source folder not found: {source_folder}"
            )

        images = get_images(source_folder)

        random_generator.shuffle(images)

        total_images = len(images)

        train_count = int(total_images * TRAIN_RATIO)
        validation_count = int(total_images * VALIDATION_RATIO)

        train_images = images[:train_count]

        validation_images = images[
            train_count:
            train_count + validation_count
        ]

        test_images = images[
            train_count + validation_count:
        ]

        train_class_folder = TRAIN_DIR / output_class
        validation_class_folder = VALIDATION_DIR / output_class
        test_class_folder = TEST_DIR / output_class

        prepare_destination_folder(train_class_folder)
        prepare_destination_folder(validation_class_folder)
        prepare_destination_folder(test_class_folder)

        for image in train_images:
            shutil.copy2(
                image,
                train_class_folder / image.name
            )

        for image in validation_images:
            shutil.copy2(
                image,
                validation_class_folder / image.name
            )

        for image in test_images:
            shutil.copy2(
                image,
                test_class_folder / image.name
            )

        total_train += len(train_images)
        total_validation += len(validation_images)
        total_test += len(test_images)

        print(f"{output_class}:")
        print(f"  Total:      {total_images}")
        print(f"  Train:      {len(train_images)}")
        print(f"  Validation: {len(validation_images)}")
        print(f"  Test:       {len(test_images)}")
        print()

    print("--------------------------------")
    print("Dataset preparation completed.")
    print("--------------------------------")
    print(f"Train images:      {total_train}")
    print(f"Validation images: {total_validation}")
    print(f"Test images:       {total_test}")
    print(
        f"Total images:      "
        f"{total_train + total_validation + total_test}"
    )


if __name__ == "__main__":
    split_dataset()