#Trim Cell Images Parasitized

from PIL import Image
import os
count = 0
directory = "C:\\Users\\sumea\\Downloads\\cell_images\\cell_images"
os.chdir(directory + "\\resized_images\\Parasitized")
for img in os.listdir(directory + "\\Parasitized"):
    pil_img = Image.open(directory + "\\Parasitized\\" + img)
    resized = pil_img.resize((100,100))
    resized.save("img" + str(count) + ".png", "PNG")
    count += 1
