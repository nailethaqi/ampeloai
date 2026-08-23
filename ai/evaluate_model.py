from pathlib import Path

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
MODEL_PATH = PROJECT_ROOT / "model" / "grape_model.keras"
RESULTS_DIR = PROJECT_ROOT / "thesis-assets" / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32

print("\nLoading test dataset...\n")

test_dataset = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    shuffle=False
)

class_names = test_dataset.class_names

print("\nClasses:")
for index, class_name in enumerate(class_names):
    print(f"{index}: {class_name}")

print("\nLoading trained model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully.")

print("\nEvaluating model on test dataset...\n")

test_loss, test_accuracy = model.evaluate(
    test_dataset,
    verbose=1
)

print("\n------------------------------")
print("FINAL TEST RESULTS")
print("------------------------------")

print(f"Test Accuracy: {test_accuracy * 100:.2f}%")
print(f"Test Loss:     {test_loss:.4f}")

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
    digits=4
)

print("\nClassification Report:\n")
print(report)

report_path = RESULTS_DIR / "classification_report.txt"

with open(
    report_path,
    "w",
    encoding="utf-8"
) as file:

    file.write("GRAPE LEAF DISEASE CLASSIFICATION REPORT\n")
    file.write("========================================\n\n")

    file.write(
        f"Test Accuracy: {test_accuracy * 100:.2f}%\n"
    )

    file.write(
        f"Test Loss: {test_loss:.4f}\n\n"
    )

    file.write(report)

matrix = confusion_matrix(
    true_labels,
    predicted_labels
)

display = ConfusionMatrixDisplay(
    confusion_matrix=matrix,
    display_labels=class_names
)

display.plot(
    xticks_rotation=30
)

plt.title(
    "Confusion Matrix - Grape Leaf Disease Classification"
)

plt.tight_layout()

confusion_matrix_path = (
    RESULTS_DIR / "confusion_matrix.png"
)

plt.savefig(
    confusion_matrix_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

metrics_path = RESULTS_DIR / "test_metrics.txt"

with open(
    metrics_path,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        f"Test Accuracy: {test_accuracy * 100:.2f}%\n"
    )

    file.write(
        f"Test Loss: {test_loss:.4f}\n"
    )

print("\nResults saved successfully:")
print(report_path)
print(confusion_matrix_path)
print(metrics_path)

print("\nModel evaluation completed.")