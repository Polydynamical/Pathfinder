import sys
import json
from math import pi, cos, asin, sqrt
import numpy as np
from datetime import datetime

start = sys.argv[1]
end = sys.argv[2]

starttime = datetime.now()
print("Loading Data...")
tree = json.loads(open("../Data/Nodes/san_mateo_county_adjacency_list.txt").read())
endtime = datetime.now()
print(f"Data loading took {endtime-starttime}s!\n")

def distance(latlon1, latlon2):
    lat1, lon1 = latlon1.split(",")
    lat2, lon2 = latlon2.split(",")
    lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)
    p = pi/180
    a = 0.5 - cos( (lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p))/2
    return 3958.8 * asin(sqrt(a))

print(f"Starting heuristic calculations...")
starttime = datetime.now()
heuristic = {}
for coord in tree.keys():
    heuristic[coord] = float(distance(coord, end))
endtime = datetime.now()
print(f"Heuristic Calculations took {endtime-starttime}s!\n")
# heuristic = {'S': 8, 'A': 8, 'B': 4, 'C': 3, 'D': 5000, 'E': 5000, 'G': 0}

cost = {start: 0}             # total cost for nodes visited

def AStarSearch():
    global tree, heuristic
    closed = np.array([])             # closed nodes
#    closed = []
    opened = np.array([[start, heuristic[start]]]) # opened nodes; len 1
#    opened = [[start, heuristic[start]]]
    # print(type(heuristic[start]))

    '''find the visited nodes'''
    while True:
        fn = [i[1] for i in opened]     # fn = f(n) = g(n) + h(n)
#        print(f"opened: {opened}")
#        print(f"fn: {fn}")
        chosen_index = fn.index(min(fn))
        node = opened[chosen_index][0]  # current node
        closed = np.append(closed, opened[chosen_index]) # closed.append(opened[chosen_index])

        opened = list(opened)
        del opened[chosen_index]
        opened = np.array(opened)

        if closed[-1][0] == end:        # break the loop if node G has been found
            break
        temparr = [closed_item[0] for closed_item in closed]
        for item in tree[node]:
            if item[0] in temparr:
                continue
            # print(f"item[0] = {item[0]} and is type {type(item[0])}")
            cost.update({item[0]: cost[node] + item[1]})            # add nodes to cost dictionary
            fn_node = cost[node] + heuristic[item[0]] + item[1]     # calculate f(n) of current node
            temp = [item[0], fn_node]
            opened = list(opened)
            opened.append(temp)
            opened = np.array(opened)
#            opened = np.array([opened].append(temp))
#            opened = np.append(opened, temp, axis=0)  #opened.append(temp)  # store f(n) of current node in array opened

    '''find optimal sequence'''
    trace_node = end                        # correct optimal tracing node, initialize as node G
    optimal_sequence = [end]                # optimal node sequence
    for i in range(len(closed)-2, -1, -1):
        check_node = closed[i][0]           # current node
        if trace_node in [children[0] for children in tree[check_node]]:
            children_costs = [temp[1] for temp in tree[check_node]]
            children_nodes = [temp[0] for temp in tree[check_node]]

            '''check whether h(s) + g(s) = f(s). If so, append current node to optimal sequence
            change the correct optimal tracing node to current node'''
            if cost[check_node] + children_costs[children_nodes.index(trace_node)] == cost[trace_node]:
                optimal_sequence.append(check_node)
                trace_node = check_node
    optimal_sequence.reverse()              # reverse the optimal sequence

    return closed, optimal_sequence


def main():
    print("Starting A* Search...")
    starttime = datetime.now()
    visited_nodes, optimal_nodes = AStarSearch()
    endtime = datetime.now()
    print(f"A* Search took {endtime-starttime}s!\n")
#    print('visited nodes: ' + str(visited_nodes))
    print('optimal nodes sequence: ' + str(optimal_nodes))

if __name__ == '__main__':
    main()
