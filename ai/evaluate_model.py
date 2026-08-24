from pathlib import Path
import json

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

TEST_DIR = PROJECT_ROOT / "dataset" / "test"

MODEL_DIR = PROJECT_ROOT / "model"
MODEL_PATH = MODEL_DIR / "grape_model.keras"
CLASS_NAMES_PATH = MODEL_DIR / "class_names.json"

RESULTS_DIR = PROJECT_ROOT / "thesis-assets" / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32

EXPECTED_CLASSES = [
    "Black_Rot",
    "Esca",
    "Healthy",
    "Leaf_Blight",
    "Other"
]


print("\nLoading test dataset...\n")

test_dataset = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    shuffle=False
)

dataset_class_names = test_dataset.class_names


print("\nClasses detected in test dataset:")

for index, class_name in enumerate(dataset_class_names):
    print(f"{index}: {class_name}")


if dataset_class_names != EXPECTED_CLASSES:
    raise ValueError(
        "\nUnexpected class order in test dataset.\n"
        f"Expected: {EXPECTED_CLASSES}\n"
        f"Detected: {dataset_class_names}"
    )


if not CLASS_NAMES_PATH.exists():
    raise FileNotFoundError(
        "\nclass_names.json was not found.\n"
        "Train the new 5-class model first."
    )


with open(
    CLASS_NAMES_PATH,
    "r",
    encoding="utf-8"
) as file:
    model_class_names = json.load(file)


if model_class_names != dataset_class_names:
    raise ValueError(
        "\nClass order mismatch.\n"
        f"Model classes: {model_class_names}\n"
        f"Test classes: {dataset_class_names}"
    )


class_names = model_class_names


print("\nLoading trained model...")

model = tf.keras.models.load_model(
    MODEL_PATH
)

print("Model loaded successfully.")


output_classes = model.output_shape[-1]

if output_classes != len(class_names):
    raise ValueError(
        "\nModel output does not match the number of classes.\n"
        f"Model outputs: {output_classes}\n"
        f"Expected classes: {len(class_names)}\n"
        "Retrain the model using the new 5-class dataset."
    )


print("\nEvaluating model on test dataset...\n")

test_loss, test_accuracy = model.evaluate(
    test_dataset,
    verbose=1
)


print("\n------------------------------")
print("FINAL TEST RESULTS")
print("------------------------------")

print(
    f"Test Accuracy: "
    f"{test_accuracy * 100:.2f}%"
)

print(
    f"Test Loss:     "
    f"{test_loss:.4f}"
)


true_labels = np.concatenate(
    [
        labels.numpy()
        for _, labels in test_dataset
    ]
)


predictions = model.predict(
    test_dataset,
    verbose=1
)


predicted_labels = np.argmax(
    predictions,
    axis=1
)


report = classification_report(
    true_labels,
    predicted_labels,
    target_names=class_names,
    digits=4,
    zero_division=0
)


print("\nClassification Report:\n")
print(report)


report_path = (
    RESULTS_DIR /
    "classification_report.txt"
)


with open(
    report_path,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "AMPELOAI IMAGE CLASSIFICATION REPORT\n"
    )

    file.write(
        "====================================\n\n"
    )

    file.write(
        "Classes:\n"
    )

    for index, class_name in enumerate(
        class_names
    ):
        file.write(
            f"{index}: {class_name}\n"
        )

    file.write("\n")

    file.write(
        f"Test Accuracy: "
        f"{test_accuracy * 100:.2f}%\n"
    )

    file.write(
        f"Test Loss: "
        f"{test_loss:.4f}\n\n"
    )

    file.write(report)


matrix = confusion_matrix(
    true_labels,
    predicted_labels,
    labels=range(len(class_names))
)


figure, axis = plt.subplots(
    figsize=(9, 7)
)


display = ConfusionMatrixDisplay(
    confusion_matrix=matrix,
    display_labels=class_names
)


display.plot(
    ax=axis,
    xticks_rotation=30,
    values_format="d"
)


axis.set_title(
    "Confusion Matrix - AmpeloAI Image Classification"
)

figure.tight_layout()


confusion_matrix_path = (
    RESULTS_DIR /
    "confusion_matrix.png"
)


figure.savefig(
    confusion_matrix_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close(figure)


metrics_path = (
    RESULTS_DIR /
    "test_metrics.txt"
)


with open(
    metrics_path,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "AMPELOAI TEST METRICS\n"
    )

    file.write(
        "=====================\n\n"
    )

    file.write(
        f"Test Accuracy: "
        f"{test_accuracy * 100:.2f}%\n"
    )

    file.write(
        f"Test Loss: "
        f"{test_loss:.4f}\n"
    )


print("\nResults saved successfully:")

print(report_path)
print(confusion_matrix_path)
print(metrics_path)

print("\nModel evaluation completed.")