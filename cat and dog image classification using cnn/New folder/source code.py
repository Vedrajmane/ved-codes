import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt

# Load and preprocess the dataset
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.cifar10.load_data()

# Squeeze the labels to remove the extra dimension
train_labels = train_labels.squeeze()
test_labels = test_labels.squeeze()

# Filter out only the cat and dog images
cat_dog_train_indices = (train_labels == 3) | (train_labels == 5)
cat_dog_test_indices = (test_labels == 3) | (test_labels == 5)

cat_dog_train_images = train_images[cat_dog_train_indices]
cat_dog_train_labels = train_labels[cat_dog_train_indices]
cat_dog_test_images = test_images[cat_dog_test_indices]
cat_dog_test_labels = test_labels[cat_dog_test_indices]

# Re-label the classes (0 for cat, 1 for dog)
cat_dog_train_labels = np.where(cat_dog_train_labels == 3, 0, 1)
cat_dog_test_labels = np.where(cat_dog_test_labels == 3, 0, 1)

# Normalize the pixel values to be between 0 and 1
cat_dog_train_images = cat_dog_train_images / 255.0
cat_dog_test_images = cat_dog_test_images / 255.0

# Build the CNN model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(1)  # Binary classification (cat vs dog)
])

# Compile the model
model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Train the model
history = model.fit(cat_dog_train_images, cat_dog_train_labels, epochs=10,
                    validation_data=(cat_dog_test_images, cat_dog_test_labels))

# Evaluate the model
test_loss, test_acc = model.evaluate(cat_dog_test_images, cat_dog_test_labels, verbose=2)
print('Test Accuracy:', test_acc)

# Function to load and preprocess image
def load_and_preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(32, 32))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

# Function to predict the class of an image
# Function to predict the class of an image
def predict_image_class(image_path):
    img_array = load_and_preprocess_image(image_path)
    predictions = model.predict(img_array)
    score = tf.nn.sigmoid(predictions[0])
    score = score.numpy()[0]  # Convert tensor to numpy array and get the scalar value
    if score < 0.5:
        print(f'This is a cat with a {100 * (1 - score):.2f}% confidence.')
    else:
        print(f'This is a dog with a {100 * score:.2f}% confidence.')


# Example usage
image_path = r'Images/12.jpg'  # Replace with your image path
predict_image_class(image_path)

# Plot training history
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')
plt.show()
