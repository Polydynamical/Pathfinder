import sys
from datetime import datetime
import numpy as np
import os
import json
from shapely.geometry import LineString, mapping
import geopandas as gpd
from matplotlib import pyplot as plt
from math import pi, cos, asin, sqrt

start = sys.argv[1]
end = sys.argv[2]
margin = float(sys.argv[3])

# TODO: use newton's method to find optimal critical value?!!
# GOAL MAXIMIZE node + node + node value
critical_value = 0.3 # the almighty percolation theory p value

# This first draft will only find route with most vegetation
starttime = datetime.now()
print("Loading Data...")
basefilename = "100vegetation"
original_tree = dict(json.loads(open(f"../../Data/Nodes/adjacency_lists/{basefilename}.txt").read())) # no pun intended
tree = original_tree.copy()


# data :=  parent_node: **[**[adjacent_node, scenicness_to_parent_node]]
endtime = datetime.now()
print(f"Data loading took {endtime-starttime}s!\n")


def distance(latlon1, latlon2):
    lat1, lon1 = latlon1.split(",")
    lat2, lon2 = latlon2.split(",")
    lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)
    p = pi/180
    a = 0.5 - cos( (lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p))/2
    d = 2 * 3958.8 * asin(sqrt(a))
    return d

total_distance = distance(start, end)

# Let's make a subtree with the given margin! (reduce search space). 
# (will work on this later since I don't want to rely on A* search/api.
# (Simply adding a margin will not work for obscure routes. I.e. where 
# (shortest drivable distance) >>>> (Euclidean distance) )

"""
print(len(tree.items()))
for i, x in enumerate(tree.copy().items()):
    for adj_node in x[1]:
        if distance(start, adj_node[0]) > margin:
            tree.pop(x[0])
print(len(tree.items()))
"""


# Let's eliminate nodes below our critical value! (remove unfavorable scenery)

print(len(tree.items()))

for i, x in enumerate(list(original_tree.items())):
    if x[0] == start or x[0] == end:
        continue
    x1 = x[1].copy()
    for j, y in enumerate(x1):
        if y[0] == start or y[0] == end:
            continue
        if y[1] < critical_value:
            tree[x[0]].remove(y)
            if len(tree[x[0]]) == 0:
                del tree[x[0]]

print(len(tree.items()))

# TODO: make this function into a class
def visualize(x, y):
    x_ticks = [-122.50, -122.45, -122.40, -122.35, -122.30, -122.25, -122.20, -122.15, -122.10]
    y_ticks = [37.1, 37.2, 37.3, 37.4, 37.5, 37.6, 37.7]
    line_shapes = "../../Data/tiger/tl_2021_06081_roads.shp"

    gdf = gpd.read_file(line_shapes) #POINTS

    gdf.plot(figsize=(300,100))
    plt.xlim([-122.60, -122.00])
    plt.ylim([37.0, 37.8])
    plt.scatter(x, y, color='red')
    filename = f'p{critical_value}_{basefilename}_{start}_{end}.png'
    plt.savefig(filename)

    # must have the "feh" image viewer
    os.system(f"feh {filename}")

scenic_nodes = [x[0] for x in tree.items()]

for i, x in enumerate(scenic_nodes):
    scenic_nodes[i] = [float(x.split(",")[0]), float(x.split(",")[1])]

scenic_nodes = np.asarray(scenic_nodes)
visualize(scenic_nodes[:,1], scenic_nodes[:,0])

# Let's find the 
