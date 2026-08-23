from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input




PROJECT_ROOT = Path(__file__).resolve().parent.parent

TRAIN_DIR = PROJECT_ROOT / "dataset" / "train"
VALIDATION_DIR = PROJECT_ROOT / "dataset" / "validation"

MODEL_DIR = PROJECT_ROOT / "model"
RESULTS_DIR = PROJECT_ROOT / "thesis-assets" / "results"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "grape_model.keras"

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 15
SEED = 42




print("\nLoading training dataset...")

train_dataset = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    shuffle=True,
    seed=SEED
)

print("\nLoading validation dataset...")

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    VALIDATION_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    shuffle=False
)

class_names = train_dataset.class_names
number_of_classes = len(class_names)

print("\nClasses detected:")
for index, class_name in enumerate(class_names):
    print(f"{index}: {class_name}")




training_labels = []

for _, labels in train_dataset.unbatch():
    training_labels.append(int(labels.numpy()))

training_labels = np.array(training_labels)

weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(training_labels),
    y=training_labels
)

class_weights = {
    index: weight
    for index, weight in enumerate(weights)
}

print("\nClass weights:")
print(class_weights)




AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(
    buffer_size=AUTOTUNE
)

validation_dataset = validation_dataset.prefetch(
    buffer_size=AUTOTUNE
)




data_augmentation = tf.keras.Sequential(
    [
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.10),
        layers.RandomZoom(0.10),
        layers.RandomContrast(0.10)
    ],
    name="data_augmentation"
)




base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)


base_model.trainable = False




inputs = tf.keras.Input(
    shape=(224, 224, 3)
)

x = data_augmentation(inputs)

x = preprocess_input(x)

x = base_model(
    x,
    training=False
)

x = layers.GlobalAveragePooling2D()(x)

x = layers.Dropout(0.30)(x)

outputs = layers.Dense(
    number_of_classes,
    activation="softmax"
)(x)

model = tf.keras.Model(
    inputs,
    outputs
)




model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

print("\nModel architecture:\n")

model.summary()




callbacks = [

    tf.keras.callbacks.ModelCheckpoint(
        filepath=MODEL_PATH,
        monitor="val_accuracy",
        save_best_only=True,
        mode="max",
        verbose=1
    ),

    tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=4,
        restore_best_weights=True,
        verbose=1
    ),

    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=2,
        min_lr=0.00001,
        verbose=1
    )
]




print("\nStarting model training...\n")

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=EPOCHS,
    class_weight=class_weights,
    callbacks=callbacks
)




model.save(MODEL_PATH)

print("\nModel saved successfully:")
print(MODEL_PATH)




training_accuracy = history.history["accuracy"]
validation_accuracy = history.history["val_accuracy"]

training_loss = history.history["loss"]
validation_loss = history.history["val_loss"]

epochs_range = range(
    1,
    len(training_accuracy) + 1
)


plt.figure(figsize=(8, 5))

plt.plot(
    epochs_range,
    training_accuracy,
    label="Training Accuracy"
)

plt.plot(
    epochs_range,
    validation_accuracy,
    label="Validation Accuracy"
)

plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("Model Training Accuracy")
plt.legend()
plt.tight_layout()

accuracy_path = RESULTS_DIR / "training_accuracy.png"

plt.savefig(
    accuracy_path,
    dpi=300
)

plt.close()


plt.figure(figsize=(8, 5))

plt.plot(
    epochs_range,
    training_loss,
    label="Training Loss"
)

plt.plot(
    epochs_range,
    validation_loss,
    label="Validation Loss"
)

plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Model Training Loss")
plt.legend()
plt.tight_layout()

loss_path = RESULTS_DIR / "training_loss.png"

plt.savefig(
    loss_path,
    dpi=300
)

plt.close()


print("\nGraphs saved successfully:")
print(accuracy_path)
print(loss_path)

print("\nTraining completed successfully.")