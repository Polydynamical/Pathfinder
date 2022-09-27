from math import cos, asin, sqrt, pi
import os

def distance(latlon1, latlon2):
    lat1, lon1 = latlon1.split(",")
    lat2, lon2 = latlon2.split(",")
    lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 3958.8 * asin(sqrt(a)) # number of miles

filelines = open("locations.txt").readlines()
for i, x in enumerate(filelines):
    filelines[i] = x.replace("\n", "")

for i, x in enumerate(filelines):
    if x == "[" or x == "]":
        continue

    try:
        filelines[i] = f"{x.split(' ')[1]},{x.split(' ')[0]}"
    except:
        print(i)

adjacency_dict = {}

for i, line in enumerate(filelines):
    if i == 0 or i == 250841:
        continue
    if filelines[i] == "[" or filelines[i] == "]":
        continue

    if filelines[i - 1] == "[":
        if line in adjacency_dict.keys():
            adjacency_dict[line].append([filelines[i + 1], distance(line, filelines[i + 1])])
        else:
            adjacency_dict[line] = []
            adjacency_dict[line].append([filelines[i + 1], distance(line, filelines[i + 1])])
    elif filelines[i + 1] == "]":
        if line in adjacency_dict.keys():
            adjacency_dict[line].append([filelines[i - 1], distance(line, filelines[i - 1])])
        else:
            adjacency_dict[line] = []
            adjacency_dict[line].append([filelines[i - 1], distance(line, filelines[i - 1])])
    elif filelines[i - 1] != "[" and filelines[i + 1] != "]":
        if line in adjacency_dict.keys():
            adjacency_dict[line].append([filelines[i - 1], distance(line, filelines[i - 1])])
            adjacency_dict[line].append([filelines[i + 1], distance(line, filelines[i + 1])])
        else:
            adjacency_dict[line] = []
            adjacency_dict[line].append([filelines[i - 1], distance(line, filelines[i - 1])])
            adjacency_dict[line].append([filelines[i + 1], distance(line, filelines[i + 1])])
    else:
        print(f"error on line #{i} because the line is {line}")

# print("{" + "\n".join("{!r}: {!r},".format(key, value) for key, value in adjacency_dict.items()) + "}", file=open("san_mateo_county_adjacency_list.txt", "a"))
# print(str(adjacency_dict), file=open("san_mateo_county_adjacency_list.py", "a"))
