from keras.models import Sequential, load_model
from keras.layers import Dense, Convolution2D, MaxPooling2D, Flatten, BatchNormalization
import glob
import cv2
import numpy as np
from tqdm import tqdm
from sklearn.metrics import accuracy_score
import random

# Training variables
batch_size = 64
classes = ["parasitized", "uninfected"]
num_classes = len(classes)
epochs = 5
kernel_size = 5
pool_size = 2
strides = 1
img_width, img_height = 100, 100
training_random, testing_random = np.random.randint(low=1, high=100, size=2)

# Create a list to store all the images and their labels
# Labels are represented as [probability of Uninfected, probability of Parasitized]
train_images = []
train_labels = []
test_images = []
test_labels = []

try:
	# If the data is already stored, load the existing data
	train_images = np.load("train_images.npy")
	train_labels = np.load("train_labels.npy")
	test_images = np.load("test_images.npy")
	test_labels = np.load("test_labels.npy")
	
except Exception:
	# For each "uninfected" cell, save the image and its label to the data lists
	count = 1
	for uninfected_img in tqdm(glob.glob("C:\\Users\\sumea\\Downloads\\cell_images\\cell_images\\resized_images\\Uninfected\\*.png")):
		uninfected_img = cv2.imread(uninfected_img, cv2.IMREAD_COLOR)
		if np.random.randint(low=0, high=10) < 9:
			train_images.append(np.array(uninfected_img))
			train_labels.append(np.array([1, 0]))
			count += 1
		else:
			test_images.append(np.array(uninfected_img))
			test_labels.append(np.array([1, 0]))
			
		
	# For each "parasitized" cell, save the image and its label to the data lists
	count = 1
	for parasitized_img in tqdm(glob.glob("C:\\Users\\sumea\\Downloads\\cell_images\\cell_images\\resized_images\\Parasitized\\*.png")):
		parasitized_img = cv2.imread(parasitized_img, cv2.IMREAD_COLOR)
		if np.random.randint(low=0, high=10) < 9:
			train_images.append(np.array(parasitized_img))
			train_labels.append(np.array([0, 1]))
			count += 1
		else:
			test_images.append(np.array(parasitized_img))
			test_labels.append(np.array([0, 1]))
			
	random.Random(training_random).shuffle(train_images)
	random.Random(training_random).shuffle(train_labels)
	random.Random(testing_random).shuffle(test_images)
	random.Random(testing_random).shuffle(test_labels)
	# Save the data to files so that it doesn't need to be processed every time
	np.save("train_images.npy", train_images)
	np.save("train_labels.npy", train_labels)
	np.save("test_images.npy", test_images)
	np.save("test_labels.npy", test_labels)
	# Since the data is already stored, load the existing data
	train_images = np.load("train_images.npy")
	train_labels = np.load("train_labels.npy")
	test_images = np.load("test_images.npy")
	test_labels = np.load("test_labels.npy")

print("Finished formatting data!")
print("Proceeding to create neural network model!")

# Create the convolutional neural network model
model = Sequential()

# First convolutional and max pooling layer
model.add(Convolution2D(filters=32, kernel_size=kernel_size, strides=strides, activation="relu",
                        input_shape=(img_height, img_width, 3)))
model.add(MaxPooling2D(pool_size=pool_size))
model.add(BatchNormalization())

# Second convolutional and max pooling layer
model.add(Convolution2D(filters=64, kernel_size=kernel_size, strides=strides, activation="relu"))
model.add(MaxPooling2D(pool_size=pool_size))
model.add(BatchNormalization())

# Third convolutional and max pooling layer
model.add(Convolution2D(filters=128, kernel_size=kernel_size, strides=strides, activation="relu"))
model.add(MaxPooling2D(pool_size=pool_size))
model.add(BatchNormalization())

# Shapes the data into a usable format for the next layer of the model
model.add(Flatten())

# Dropout layer prevents overfitting the model
#model.add(Dropout(rate=0.05))

# Fully connected layer with (num_classes) outputs to predict the class of the input
model.add(Dense(units=num_classes, activation="softmax"))

# Print a summary of the model to help understand the structure
print(model.summary())
# Compile the model so we can train it
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Inform the user that the model has compiled successfully
print("Finished compiling neural network!")
print("Proceeding to train neural network!")

try:
	# Try to load the existing model
	model = load_model("model.h5")
    
except Exception:
    
	# If there is an error in loading the existing model (ie, it doesn't exist), train the model
	model.fit(train_images, train_labels, batch_size=batch_size, epochs=epochs,
          validation_data=(test_images, test_labels))
	model.save("model.h5")

# Inform the user that the model has finished training
print("Finished training!")
print("Proceeding to calculate accuracy!")

# Predicts the class label for each of the test images
predicted_labels = model.predict(test_images)
predicted_labels = (predicted_labels > 0.5)

# Calculate the accuracy of the model
accuracy = accuracy_score(test_labels, predicted_labels)
print(accuracy)