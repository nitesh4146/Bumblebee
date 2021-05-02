import pandas as pd
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
from preprocess import preprocess
import torch

print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))

DATA_DIR = "/home/slickmind/Documents/svl_e2e/train/maps"
DATA_CSV = "training_data.csv"
DATA_IMG = "img"
CAMERA_LIST = ["center", "right", "left"]

all_maps = glob.glob(DATA_DIR + "/*")
maps_data = []
maps_data += [glob.glob(map + "/*") for map in all_maps]

# print(maps_data)

images = []
images_flip = []

steering = []
correction = 0.02

sky_crop = 530
hood_crop = 870

img = cv2.imread("/home/slickmind/Documents/svl_e2e/train/maps/Map1/data8/img/center-2021-04-30T21:10:27.849835.jpg")
plt.imshow(preprocess(img), cmap="gray")
plt.show()
row, col, ch = preprocess(img).shape

total_images = len(glob.glob(DATA_DIR + "/**/*.jpg", recursive = True))

# tensor = torch.zeros((total_images, row, col, ch))
# if torch.cuda.is_available():
#   tensor = tensor.to('cuda')

# print(tensor.shape)

for data in maps_data[0]:                       # Iterate over each map
    csv_df = pd.read_csv(data + "/" + DATA_CSV, header=None)
    print("loading ", data)

    for index, row in csv_df.iterrows():        # Iterate over data for each map
        img_time = row[0]
        steer = row[1]

        for i in range(3):
            img_path = data + "/" + DATA_IMG + "/" + CAMERA_LIST[i] + "-" + img_time + ".jpg"
            img = cv2.imread(img_path)
            img_processed = preprocess(img)
            # print(img_processed.shape)

            images.append(img_processed)
            images_flip.append(np.fliplr(img_processed))

        steering.append(float(row[1]))                 # Corresponds to Center Image
        steering.append(float(row[1]) + correction)    # Corresponds to Right Image
        steering.append(float(row[1]) - correction)    # Corresponds to Left Image


# with open('data.pkl','wb') as f:
#     pickle.dump([new_images, new_measurements], f)

print(len(images))
print(len(steering))
