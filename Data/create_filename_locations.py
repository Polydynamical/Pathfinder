# for each location, replace the ID with its corresponding image name

import json
import numpy as np
import tqdm

out = open("filename_locations.json", "a")

links = open("unique_image_links.txt").readlines()
stuff = np.array(json.loads(open("san_mateo_county_GSV.json").read()))
locations, IDs = stuff[:,0], stuff[:,1]

for i, link in enumerate(links):
    links[i] = link.split("&panoid=")[1].split("&x=")[0]

for j, location in tqdm.tqdm(enumerate(locations)):
    out.write(str([location, str(links.index(IDs[j]) // 2).zfill(6)]) + "\n")
"""
print(links[0:5])
print("\n")
print(locations[0:5])
print("\n")
print(IDs[0:5])
print("\n")



print(len(links))
print("\n")
print(len(locations))
print("\n")
print(len(IDs))
print("\n")

"""
