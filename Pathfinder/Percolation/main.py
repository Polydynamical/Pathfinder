import sys
import tqdm
import seaborn
from random import shuffle
import statistics as stats
from datetime import datetime
import numpy as np
import os
import json
from shapely.geometry import LineString, mapping
import geopandas as gpd
from matplotlib import pyplot as plt
from math import radians, degrees, pi, acos, cos, sin, asin, atan2, sqrt

R = 3958.899 # Radius of earth in miles

# bring in A*

# ('[float0],[float1]') -> (float0, float1)
def str_to_tuple(tmp: str) -> tuple:
    return tuple([float(x) for x in tuple(tmp.split(","))])

def tuple_to_str(tmp: tuple) -> str:
    return str(tmp).replace("(","").replace(")","").replace(" ","")

start = sys.argv[1]
end = sys.argv[2]
# margin = float(sys.argv[3]) # Maybe develop algorithm to set margin based on distance to destination. Maybe 1.5 times the distance? Or maybe based on # of nodes/time. YUP (see "find reasonable clusters" in "percolation search" below. (Use a circle as radius from midpoint of start/end nodes))
e = float(sys.argv[3]) # eccentricity of ellipse bound
p = float(sys.argv[4])


# TODO: use newton's method to find optimal critical value?!!
# GOAL MAXIMIZE node + node + node value
critical_value = p # the almighty percolation theory p value

# This first draft will only find route with most vegetation
starttime = datetime.now()
print("Loading Data...")
basefilename = "100vegetation"
original_tree = dict(json.loads(open(f"../../Data/Nodes/adjacency_lists/{basefilename}.txt").read())) # no pun intended
tree = original_tree.copy()


# data :=  parent_node: **[**[adjacent_node, scenicness_to_parent_node]]
endtime = datetime.now()
print(f"Data loading took {endtime-starttime}s!\n")

    
def haversine_from_angle(theta: float) -> float:
    return 0.5 * (1 - cos(theta))

def haversine_from_coords(lat1: float, lat2: float, lon1: float, lon2: float) -> float:
    return sqrt( haversine_from_angle( (lat2 - lat1) * pi/180) + cos(lat1 * pi/180) * cos(lat2 * pi/180) * (haversine_from_angle( (lon2 - lon1) * pi/180)) )

def distance(latlon1: str, latlon2: str) -> float:
    lat1, lon1 = latlon1.split(",")
    lat2, lon2 = latlon2.split(",")
    lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)
    a = haversine_from_coords(lat1, lat2, lon1, lon2)
    d = 2 * R * asin(a)
    return d

total_distance = distance(start, end)

def midpoint(latlon1: str, latlon2: str) -> str:
    lat1, lon1 = latlon1.split(",")
    lat2, lon2 = latlon2.split(",")
    lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))


    bx = cos(lat2) * cos(lon2 - lon1)
    by = cos(lat2) * sin(lon2 - lon1)

    lat_m = atan2( sin(lat1) + sin(lat2), sqrt( (cos(lat1) + bx) ** 2 + by ** 2) )
    lon_m = lon1 + atan2(by, cos(lat1) + bx)
    
    return tuple_to_str((degrees(lat_m), degrees(lon_m)))



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

print(f"# of Regular Nodes: {len(tree.items())}")

for i, x in tqdm.tqdm(enumerate(list(original_tree.items())), desc="Scenic Nodes"):
    if x[0] == start or x[0] == end:
        continue
    x1 = x[1].copy()
    for j, y in enumerate(x1):
#        if y[0] == start or y[0] == end:
#            continue
        if y[1] < critical_value:
            tree[x[0]].remove(y)
            if len(tree[x[0]]) == 0:
                del tree[x[0]]

print(f"# of Scenic Nodes: {len(tree.items())}")

# TODO: make this function into a class
def visualize(coords):
    coords = np.asarray(coords)
    x, y = coords[:,1], coords[:,0] # latitude are horizontal lines that give vertical position & longitude are vertical lines that give horizontal position
    x_ticks = [-122.50, -122.45, -122.40, -122.35, -122.30, -122.25, -122.20, -122.15, -122.10]
    y_ticks = [37.1, 37.2, 37.3, 37.4, 37.5, 37.6, 37.7]
    line_shapes = "../../Data/tiger/tl_2021_06081_roads.shp"

    gdf = gpd.read_file(line_shapes) #POINTS

    gdf.plot(figsize=(300,100))
    plt.xlim([-122.60, -122.00])
    plt.ylim([37.0, 37.8])
    plt.scatter(x, y, color='red')
    plt.scatter([float(start.split(",")[1])], [float(start.split(",")[0])], color='green')
    plt.scatter([float(end.split(",")[1])], [float(end.split(",")[0])], color='green')
    filename = f'out/p{critical_value}_{basefilename}_{start}_{end}.png'
    plt.savefig(filename)

    # must have the "feh" image viewer
#    os.system(f"feh {filename}")

scenic_nodes = [x[0] for x in tree.items()]

for i, x in enumerate(scenic_nodes):
    scenic_nodes[i] = [float(x.split(",")[0]), float(x.split(",")[1])]

# visualize(scenic_nodes)

scenic_tuple_nodes = []
for i, x in enumerate(scenic_nodes):
    scenic_tuple_nodes.append(tuple(x))

legend = {}
for i, location in enumerate(scenic_tuple_nodes):
    legend[i] = location

# Let's find th highest value of scenicness with from start to finish (with a given mile limit)

# we can also check cluster size by checking which two scenic nodes (subset of all nodeS) are adjacent to check the largest cluster size
# A way of searching for the best route maybe we can create a system where the p-value will be optimized by the largest cluster size for 
# the route from start to end.

# FOR LIMIT!!! We can find the average lenght of an edge (have already calculated distance between nodes) for ALL nodes in the road dataset, say x. (verify with standard deviation that the average is a good measure).
# Then, we simply count the number of nodes visited as our distance metric (rather than Euclidean distance). 
# Excluding the top and bottom 1000 values, all values are within one standard deviation from mean.


# NAH Buddy. This is similar to the Traveling Salesman Problem. 

# Idea: You have all the scenic nodes/edges. Draw a line from endpoint to endpoint. Iteratively update the line function into a polynomial to fit the scenic nodes along the road edges (sort of like machine learning). 
# Maybe start with the shortest distance possible and then continue adjusting until all nodes are included.
# IDEA: Percolation search. You randomly choose nodes to close and see if they connect but force scenic nodes to stay open. This introduces randomness/scenicness aspect to the drive WOAH. <- IMPORTANT
# IDEA: GRadient search. Think of each node/edge with an elevation point and find the overall "deepest" route. (BACKPROPGATION?!)



#### Percolation Search ####

## Find Adjacent Clusters ##

# Input: Scenic Nodes in List
# Output: List of Clusters of nodes given by the connecting nodes
# Goal: Determine which nodes are adjacent to each other in scenic nodes list

# Then we should measure the distanec to a cluster frmo the start and end location and figure out if it's worth it

clusters = []
for scenic_node in tqdm.tqdm(scenic_tuple_nodes, desc="Scenic Clusters"):
    tmp = [scenic_node]
    for adjacent_scenic_node in tree[tuple_to_str(scenic_node)]:
        if (tmp2 := tuple([float(x) for x in str_to_tuple(adjacent_scenic_node[0])])) in scenic_tuple_nodes:
            tmp.append(tmp2)
    tmp.sort()
    if tmp in clusters:
        continue
    clusters.append(tmp)
print(f"# of Scenic Clusters: {len(clusters)}")

# visualize size of clusters
# seaborn.displot(np.array([len(x) for x in clusters]))


## Find Reasonable Clusters ## 

# First find average coordinate value for each cluster. (directional statisitcs)
# See https://math.stackexchange.com/questions/47854/calculate-average-latitude-longitude
cluster_avg = []
for cluster in clusters:
    points = []
    for point in cluster:
        lat1 = radians(point[0])
        lon1 = radians(point[1])
        points.append((R * cos(lat1) * cos(lon1), R * cos(lat1) * sin(lon1), R * sin(lat1))) # tuple of 3D coordinates 

    points_avg = ((stats.mean([point[0] for point in points]), stats.mean([point[1] for point in points]), stats.mean([point[2] for point in points])))

    lat = degrees(atan2(points_avg[2], sqrt(points_avg[0] ** 2 + points_avg[1] ** 2)))
    lon = degrees(atan2(points_avg[1], points_avg[0]))

    cluster_avg.append((lat, lon))

# Calculate distance of average cluster value to start and end (use margins + stuff)
# Also remove all clusters outside of range
# It should:
#   1. exclude clusters in the opposite direction of goal node (behind start node)
#   2. exclude clusters way too far away

# We can solve all of these problems by finding the midpoint of the direct connection between start and end, then setting the radius to connection/2. 
# consider changing to ellipse
cluster_good = []

# find midpoint
endpoints_midpoint = midpoint(start, end)

start_to_midpoint = distance(start, endpoints_midpoint)

lat_start = float(start.split(",")[0])
lon_start = float(start.split(",")[1])
lat_end = float(end.split(",")[0])
lon_end = float(end.split(",")[1])
lat_mid = float(endpoints_midpoint.split(",")[0])
lon_mid = float(endpoints_midpoint.split(",")[1])

a = total_distance / 2
b = sqrt( (a ** 2) * ( 1 - e ** 2) )
rot = atan2(sin(lon_end - lon_start) * cos(lat_end), cos(lat_start) * sin(lat_end) - sin(lat_start) * cos(lat_end) * cos(lon_end - lon_start))

# See https://math.stackexchange.com/questions/3747965/points-within-an-ellipse-on-the-globe
for i, cluster in tqdm.tqdm(enumerate(clusters), desc="Clusters in Range"):

    lat2 = cluster_avg[i][0]
    lon2 = cluster_avg[i][1]

    # theta = acos(-2 * haversine_from_coords(lat_start, lat2, lon_start, lon2) + 1) # angle between startpoint, midpoint, and cluster average point
    # radius = b / sqrt(1 - (e * cos(theta - rot)) ** 2)

    theta = radians(90 - lat_mid)
    phi = radians(lon_mid)
    alpha = - rot
    c = sqrt(a**2 - b**2)
    gamma = c / R


    f1_x = R * (cos(alpha) * sin(gamma) * cos(phi) * cos(theta) - sin(alpha) * sin(gamma) * sin(phi) + cos(gamma) * cos(phi) * sin(theta))
    f1_y = R * (cos(alpha) * sin(gamma) * sin(phi) * cos(theta) + sin(alpha) * sin(gamma) * cos(phi) + cos(gamma) * sin(phi) * sin(theta))
    f1_z = R * (cos(gamma) * cos(theta) - cos(alpha) * sin(gamma) * sin(theta))

    f2_x = R * (-cos(alpha) * sin(gamma) * cos(phi) * cos(theta) + sin(alpha) * sin(gamma) * sin(phi) + cos(gamma) * cos(phi) * sin(theta))
    f2_y = R * (-cos(alpha) * sin(gamma) * sin(phi) * cos(theta) - sin(alpha) * sin(gamma) * cos(phi) + cos(gamma) * sin(phi) * sin(theta))
    f2_z = R * (cos(gamma) * cos(theta) + cos(alpha) * sin(gamma) * sin(theta))

    f1 = (f1_x, f1_y, f1_z)
    f2 = (f2_x, f2_y, f2_z)

    f1 = (atan2(f1[1], f1[0]), atan2(f1[2], sqrt(f1[0]**2 + f1[1]**2)))
    f2 = (atan2(f2[1], f2[0]), atan2(f2[2], sqrt(f2[0]**2 + f2[1]**2)))

    f1 = (degrees(f1[1]), degrees(f1[0]))
    f2 = (degrees(f2[1]), degrees(f2[0]))

    d1 = distance(tuple_to_str(cluster_avg[i]), tuple_to_str(f1))
    d2 = distance(tuple_to_str(cluster_avg[i]), tuple_to_str(f2))

    if d1 + d2 <= 2 * a:
        cluster_good.append(cluster)

     
#    if distance(tuple_to_str(cluster_avg[i]), endpoints_midpoint) <= radius: # FIX
#        cluster_good.append(cluster)

# print(f"# of Clusters in Range: {len(cluster_good)}")

# Visualize Good Clusters
expand_cluster_good = []
for cluster in cluster_good:
    for coord in cluster:
        expand_cluster_good.append(list(coord))

# visualize(expand_cluster_good)

# Visualize Boundary

boundary_arr = []

lat_mid = radians(lat_mid)
lon_mid = radians(lon_mid)

for theta in range(0, 360):

    theta = radians(float(theta))

    radius = b / sqrt(1 - (e * cos(theta - rot) ) ** 2 )

    delta = radius / R

    lat2 = asin( sin(lat_mid) * cos(delta) + cos(lat_mid) * sin(delta) * cos(theta))
    lon2 = lon_mid + atan2(sin(theta) * sin(delta) * cos(lat_mid), cos(delta) - sin(lat_mid) * sin(lat2))

    boundary_arr.append([degrees(lat2), degrees(lon2)])

# visualize(boundary_arr)

## Randomize Clusters ##
# This should randomly pick clusters along the route
# Should not exceed X amount of nodes

percolated_clusters = list(cluster_good)
shuffle(percolated_clusters)
percolated_clusters = percolated_clusters[0: min(len(percolated_clusters), 20)]

# Visualize Good Percolated Clusters
expand_percolated_clusters = []
for cluster in percolated_clusters:
    for coord in cluster:
        expand_percolated_clusters.append(list(coord))

#visualize(cluster_avg + boundary_arr)
#visualize(boundary_arr + scenic_nodes)
#visualize(expand_cluster_good + boundary_arr)

visualize(expand_percolated_clusters + boundary_arr)



plt.show()
exit(0)

## Path ##
# Sorted list of distances from start to average cluster coordinates
dist_start_to_clusters = []
for cluster in percolated_clusters:
    pass

# Q: Which point in the cluster do we go to?
# A* from start to cluster 1.


print(f"Starting heuristic calculations...")
starttime = datetime.now()
heuristic = {}
for coord in tqdm.tqdm(original_tree.keys(), desc="Heuristic Calculations"):
    heuristic[coord] = distance(coord, end)
endtime = datetime.now()
print(f"Heuristic Calculations took {endtime-starttime}s!\n")

cost = {start: 0}             # total cost for nodes visited


def AStarSearch():
    global count, heuristic, cost
    closed = [] # closed nodes
    opened = [[start, heuristic[start]]]
    # print(type(heuristic[start]))

    '''find the visited nodes'''
    count = 0
    while True:
        fn = [i[1] for i in opened]     # fn = f(n) = g(n) + h(n)
        if count % 1000 == 0:
            print(len(fn))
            print(heuristic[min(np.array(opened)[:,0])])
        chosen_index = fn.index(min(fn))
        node = opened[chosen_index][0]  # current node
        closed.append(opened[chosen_index]) # closed.append(opened[chosen_index])

        del opened[chosen_index]

        if closed[-1][0] == end:        # break the loop if node G has been found
            break
        temparr = [closed_item[0] for closed_item in closed]
        for item in tree[node]:
            if item[0] in temparr:
                continue
            cost[item[0]] = cost[node] + item[1]
            #cost.update({item[0]: cost[node] + item[1]})            # add nodes to cost dictionary
            fn_node = cost[node] + heuristic[item[0]]     # calculate f(n) of current node
            temp = [item[0], fn_node]
            opened.append(temp)
        count += 1

    '''find optimal sequence'''
    trace_node = end                        # correct optimal tracing node, initialize as node G
    optimal_sequence = [end]                # optimal node sequence
    for i in range(len(closed)-2, -1, -1):
        check_node = closed[i][0]           # current node
        if trace_node in [children[0] for children in tree[check_node]]:
            #children_nodes, children_costs = tuple((temp[0], temp[1]) for temp in tree[check_node])
            for temp in tree[check_node]:
                children_costs = [temp[1] for temp in tree[check_node]]
                children_nodes = [temp[0] for temp in tree[check_node]]

            '''check whether h(s) + g(s) = f(s). If so, append current node to optimal sequence
            change the correct optimal tracing node to current node'''
            if cost[check_node] + children_costs[children_nodes.index(trace_node)] == cost[trace_node]:
                optimal_sequence.append(check_node)
                trace_node = check_node
    optimal_sequence.reverse()              # reverse the optimal sequence

    return closed, optimal_sequence



