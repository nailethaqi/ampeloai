from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "model" / "grape_model.keras"

IMAGE_SIZE = (224, 224)

CLASS_NAMES = [
    "Black_Rot",
    "Esca",
    "Healthy",
    "Leaf_Blight"
]



print("Loading grape disease model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully.")


def predict_image(image: Image.Image):

    # Convert image to RGB
    image = image.convert("RGB")

    # Resize to model input size
    image = image.resize(IMAGE_SIZE)

    # Convert image to numpy array
    image_array = np.array(
        image,
        dtype=np.float32
    )

    # Add batch dimension
    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    # Prediction
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

    return {
        "predicted_class": predicted_class,
        "confidence": round(
            confidence * 100,
            2
        ),
        "probabilities": all_probabilities
    }