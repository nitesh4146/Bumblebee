import os
import pandas as pd
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
from preprocess import preprocess
import torch

# Check GPU availability
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))

# Set data directories
WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = WORKING_DIR + "/maps"
DATA_CSV = "training_data.csv"
DATA_IMG = "img"
CAMERA_LIST = ["center", "right", "left"]

# Get all maps
all_maps = glob.glob(DATA_DIR + "/*")
maps_data = []
maps_data += [glob.glob(map + "/*") for map in all_maps]

images = []
images_flip = []

labels = []
correction = 0.02

img = cv2.imread(
    WORKING_DIR + "/maps/Map1/data8/img/center-2021-04-30T21:10:27.849835.jpg")
plt.imshow(preprocess(img), cmap="gray")
plt.show()
row, col, ch = preprocess(img).shape

total_images = len(glob.glob(DATA_DIR + "/**/*.jpg", recursive=True))

# tensor = torch.zeros((total_images, row, col, ch))
# if torch.cuda.is_available():
#   tensor = tensor.to('cuda')

# print(tensor.shape)

for data in maps_data[0]:                               # Iterate over each map
    csv_df = pd.read_csv(data + "/" + DATA_CSV, header=None)
    print("loading ", data)

    for index, row in csv_df.iterrows():                # Iterate over data for each map
        # First column of DATA_CSV contains image timestamp
        img_time = row[0]
        # Second column of DATA_CSV contains steering value
        steer = row[1]

        for i in range(3):                              # Reading all CAMERA_LIST images
            img_path = data + "/" + DATA_IMG + "/" + \
                CAMERA_LIST[i] + "-" + img_time + ".jpg"
            img = cv2.imread(img_path)
            img_processed = preprocess(img)

            images.append(img_processed)
            images_flip.append(np.fliplr(img_processed))

        # Corresponds to Center Image
        labels.append(float(row[1]))
        # Corresponds to Right Image
        labels.append(float(row[1]) + correction)
        # Corresponds to Left Image
        labels.append(float(row[1]) - correction)


# with open('data.pkl','wb') as f:
#     pickle.dump([new_images, new_measurements], f)

print(len(images))
print(len(labels))
