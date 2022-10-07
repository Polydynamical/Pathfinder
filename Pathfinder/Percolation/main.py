import sys
import os
import json

start = sys.argv[1]
end = sys.argv[2]
margin = int(sys.argv[3])

critical_value = 0.5 # the almighty percolation theory p value
# use newton's method to find optimal critical value?!!
# GOAL MAXIMIZE node + node + node value

# THIS FIRST DRAFT WILL ONLY FIND ROUTE WITH MOST VEGETATION
starttime = datetime.now()
print("Loading Data...")
tree = json.loads(open("../Data/Nodes/san_mateo_county_adjacency_list.txt").read()) # TODO REPLACE WITH SCENERY
# data :=  parent_node: **[**[adjacent_node, scenicness_to_parent_node]]
endtime = datetime.now()
print(f"Data loading took {endtime-starttime}s!\n")


total_distance = float('inf')

def distance(latlon1, latlon2, margin):
    lat1, lon1 = latlon1.split(",")
    lat2, lon2 = latlon2.split(",")
    lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)
    p = pi/180
    a = 0.5 - cos( (lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p))/2
    d = 2 * 3958.8 * asin(sqrt(a))
    if d - margin > total_distance:
        return float('inf')
    return d

total_distance = distance(start, end, margin)

# Let's make a subtree with the given margin!
# 1. Find shortest path

# Let's eliminate nodes below our critical value!
