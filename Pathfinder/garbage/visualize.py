from dsplot.graph import Graph
import json

tree = json.loads(open("../Data/Nodes/san_mateo_county_adjacency_list.txt").read())
graph = Graph(tree, directed=False)
graph.plot()
