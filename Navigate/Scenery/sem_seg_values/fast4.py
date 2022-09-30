import matplotlib.image as img
import numpy as np
from json import loads
import os
import tqdm

images = []
images += [each for each in os.listdir("../../../Data/Images/masks/") if each.endswith('.png')]
images = sorted(images)

ignore = os.listdir("../../../Data/Images/percents/")
colorkey = loads(open("colorkey.txt").read())

for i in tqdm.tqdm(range(3, len(images), 8)):
    image = images[i]
    if image.replace("png", "txt") in ignore:
        continue
    gsv = img.imread(f"../../../Data/Images/masks/{image}", format="JPG")
    colors, counts = np.unique(gsv.reshape(-1, 3), return_counts = True, axis = 0)

    for i, color in enumerate(colors):
        for j in range(3):
            colors[i][j] = int(colors[i][j] * 255)

    for i, x in enumerate(colors):
        colors[i] = x.tolist()

    colors = colors.tolist()

    for i, x in enumerate(colors):
        print(f"{round(((counts[i])/2621.4), 2)}%: {colorkey[str(x)]}", file=open(f"../../../Data/Images/percents/{image.replace('.png', '.txt')}", "a"))

