#!/bin/zsh
ogr2ogr -f CSV san_mateo_county.csv tl_2021_06081_roads.shp -lco GEOMETRY=AS_WKT
