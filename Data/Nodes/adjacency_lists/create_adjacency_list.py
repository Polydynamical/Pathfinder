from math import cos, asin, sqrt, pi
import tqdm
import numpy as np
import json
import os

# parameters to change
params = {"vegetation": 1.0}

filelines = open("../../locations.txt").readlines()
filename_locations = np.array(json.loads(open("../../filename_locations.json").read()))
coords, filename = list(filename_locations[:,0]), list(filename_locations[:,1])

for i, x in enumerate(filelines):
    filelines[i] = x.replace("\n", "")

for i, x in enumerate(filelines):
    if x == "[" or x == "]":
        continue


# function for creating adjacency lists based on distance between nodes
def distance(latlon1, latlon2, p0_0, p0_1, p1_0, p1_1):
    lat1, lon1 = latlon1.split(",")
    lat2, lon2 = latlon2.split(",")
    lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 3958.8 * asin(sqrt(a)) # number of miles

# Function for creating adjacency lists simply amount of vegetation
def vegetation(latlon1, latlon2, p0_0, p0_1, p1_0, p1_1):
    # divide 100
    p0_0, p0_1, p1_0, p1_1 = np.array(p0_0), np.array(p0_1), np.array(p1_0), np.array(p1_1)

    # I tried doing globals()[var] etc but it wasn't working and idc about code that much here
    try:
        p0_0_veg = float(p0_0[:,0][list(p0_0[:,1]).index("vegetation")]) / 100
    except:
        p0_0_veg = 0.0

    try:
        p0_1_veg = float(p0_1[:,0][list(p0_1[:,1]).index("vegetation")]) / 100
    except:
        p0_1_veg = 0.0

    try:
        p1_0_veg = float(p1_0[:,0][list(p1_0[:,1]).index("vegetation")]) / 100
    except:
        p1_0_veg = 0.0
    
    try:
        p1_1_veg = float(p1_1[:,0][list(p1_1[:,1]).index("vegetation")]) / 100
    except:
        p1_1_veg = 0.0

    p0_veg = 0.5 * ( p0_0_veg + p0_1_veg )
    p1_veg = 0.5 * ( p1_0_veg + p1_1_veg)

    return 0.5 * ( p0_veg + p1_veg )

functionList = {"vegetation": vegetation}


# Specify parameters as input
# kwargs here takes in the format {label}={percent contribution}
# range(percent contribution) = [-1, 1]
def scenicness(latlon1, latlon2, **kwargs):
    # average vegetation value(average vegetation(node 1), average vegetation(node 2))

    # open percent files
    p0_base = "null"
    try:
        p0_base = filename[coords.index(latlon1)]
        p0_0 = open(f"../../Images/percents/{p0_base}_0.txt").readlines()
        p0_1 = open(f"../../Images/percents/{p0_base}_1.txt").readlines()
    except:
        # there is no street view for the designated location
        p0_0 = open(f"../../Images/percents/{p0_base}.txt").readlines()
        p0_1 = open(f"../../Images/percents/{p0_base}.txt").readlines()



    p0_0 = [x.split("\n")[0].split(r"%: ") for x in p0_0]
    p0_1 = [x.split("\n")[0].split(r"%: ") for x in p0_1]
    


    p1_base = "null"
    try:
        p1_base = filename[coords.index(latlon2)]
        p1_0 = open(f"../../Images/percents/{p1_base}_0.txt").readlines()
        p1_1 = open(f"../../Images/percents/{p1_base}_1.txt").readlines()
    except:
        # there is no street view for the designated location
        p1_0 = open(f"../../Images/percents/{p1_base}.txt").readlines()
        p1_1 = open(f"../../Images/percents/{p1_base}.txt").readlines()



    p1_0 = [x.split("\n")[0].split(r"%: ") for x in p1_0]
    p1_1 = [x.split("\n")[0].split(r"%: ") for x in p1_1]

    
    total = 0
    for var, contrib in kwargs.items():
        total += contrib * functionList[var](latlon1, latlon2, p0_0, p0_1, p1_0, p1_1)

    return total

adjacency_dict = {}

# This goes through everything in locations.txt
# and calculates the heuristic between each node.
for i, line in tqdm.tqdm(enumerate(filelines), total=250177, desc="main loop"):
    if i == 0 or i == 250841:
        continue
    if filelines[i] == "[" or filelines[i] == "]":
        continue

    if filelines[i - 1] == "[":
        if line in adjacency_dict.keys():
            adjacency_dict[line].append([filelines[i + 1], scenicness(line, filelines[i + 1], **params)])
        else:
            adjacency_dict[line] = []
            adjacency_dict[line].append([filelines[i + 1], scenicness(line, filelines[i + 1], **params)])
    elif filelines[i + 1] == "]":
        if line in adjacency_dict.keys():
            adjacency_dict[line].append([filelines[i - 1], scenicness(line, filelines[i - 1], **params)])
        else:
            adjacency_dict[line] = []
            adjacency_dict[line].append([filelines[i - 1], scenicness(line, filelines[i - 1], **params)])
    elif filelines[i - 1] != "[" and filelines[i + 1] != "]":
        if line in adjacency_dict.keys():
            adjacency_dict[line].append([filelines[i - 1], scenicness(line, filelines[i - 1], **params)])
            adjacency_dict[line].append([filelines[i + 1], scenicness(line, filelines[i + 1], **params)])
        else:
            adjacency_dict[line] = []
            adjacency_dict[line].append([filelines[i - 1], scenicness(line, filelines[i - 1], **params)])
            adjacency_dict[line].append([filelines[i + 1], scenicness(line, filelines[i + 1], **params)])
    else:
        print(f"error on line #{i} because the line is {line}")

filename = ""
for x in params.items():
    filename += str(int(x[1] * 100))
    filename += x[0]

print("{" + "\n".join("{!r}: {!r},".format(key, value) for key, value in adjacency_dict.items()) + "}", file=open(f"{filename}.txt", "a"))
# print(str(adjacency_dict), file=open("san_mateo_county_adjacency_list.py", "a"))
