#Prediction Subprogram, Singular File

from keras.models import load_model
import numpy as np
import cv2
                
model = load_model("model.h5")
file_path = ""
while file_path != "quit":
    file_path = input("Enter a file path: ")
    img = cv2.imread(file_path, cv2.IMREAD_COLOR)
    cv2.imshow("test_image", img)
    output = model.predict(np.expand_dims(np.array(img), axis=0))
    print(output)
    if output[0][0] > output[0][1]:
        # Uninfected
        print("Uninfected: " + str(output[0][0] * 100) + "%")
    else:
        # Parasitic
        print("Parasitic: " + str(output[0][1] * 100) + "%")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
