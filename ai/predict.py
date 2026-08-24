from pathlib import Path
import json

import numpy as np
import tensorflow as tf
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_DIR = PROJECT_ROOT / "model"
MODEL_PATH = MODEL_DIR / "grape_model.keras"
CLASS_NAMES_PATH = MODEL_DIR / "class_names.json"

IMAGE_SIZE = (224, 224)

EXPECTED_CLASSES = [
    "Black_Rot",
    "Esca",
    "Healthy",
    "Leaf_Blight",
    "Other"
]


if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}"
    )


if not CLASS_NAMES_PATH.exists():
    raise FileNotFoundError(
        f"Class names file not found: {CLASS_NAMES_PATH}. "
        "Train the new 5-class model first."
    )


with open(
    CLASS_NAMES_PATH,
    "r",
    encoding="utf-8"
) as file:
    CLASS_NAMES = json.load(file)


if CLASS_NAMES != EXPECTED_CLASSES:
    raise ValueError(
        "\nUnexpected class configuration.\n"
        f"Expected: {EXPECTED_CLASSES}\n"
        f"Detected: {CLASS_NAMES}"
    )


print("Loading AmpeloAI model...")

model = tf.keras.models.load_model(
    MODEL_PATH
)

print("Model loaded successfully.")


if model.output_shape[-1] != len(CLASS_NAMES):
    raise ValueError(
        "\nModel output does not match class configuration.\n"
        f"Model outputs: {model.output_shape[-1]}\n"
        f"Classes: {len(CLASS_NAMES)}\n"
        "Retrain the model using the 5-class dataset."
    )


def predict_image(image: Image.Image):

    image = image.convert("RGB")

    image = image.resize(
        IMAGE_SIZE
    )

    image_array = np.array(
        image,
        dtype=np.float32
    )

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    predictions = model.predict(
        image_array,
        verbose=0
    )[0]

    predicted_index = int(
        np.argmax(predictions)
    )

    confidence = float(
        predictions[predicted_index]
    )

    predicted_class = CLASS_NAMES[
        predicted_index
    ]

    all_probabilities = {
        CLASS_NAMES[index]: round(
            float(probability) * 100,
            2
        )
        for index, probability
        in enumerate(predictions)
    }

    is_supported = (
        predicted_class != "Other"
    )

    return {
        "predicted_class": predicted_class,
        "confidence": round(
            confidence * 100,
            2
        ),
        "probabilities": all_probabilities,
        "is_supported": is_supported,
        "rejection_reason": (
            None
            if is_supported
            else "unsupported_image"
        )
    }