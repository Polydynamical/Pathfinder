from shapely.geometry import LineString, mapping
import geopandas as gpd
from matplotlib import pyplot as plt

line_shapes = "../Data/Nodes/tiger/tl_2021_06081_roads.shp"

gdf = gpd.read_file(line_shapes) #POINTS

gdf.plot(figsize=(200,50))

plt.savefig('out.png')
plt.show()
