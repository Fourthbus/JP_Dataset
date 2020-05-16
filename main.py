import geopandas as gpd
from geopandas.geoseries import *
from shapely import wkt

# gigl = gpd.read_file("GIGL/GIGL_OPS_filtered.shp")
road = gpd.read_file("Road/London road link_subtracted_Segment_Map.shp")
park = gpd.read_file("GIGL/GiGL_OPS_filtered_CopyFeatur.shp")
# roadworked = gpd.read_file("Road2/London_Road_subtracted.shp")

# pt = wkt.loads('POINT(520000 172000)')
# poly = gigl2d[: 1].geometry[0]
# line = road[: 1].geometry[0]

roadbound = road.geometry.bounds
parkbound = park.geometry.bounds

parkbound = parkbound.add(pd.Series([-50,-50,50,50], index=['minx','miny','maxx','maxy']), axis='index')

parkbound_judge = parkbound.sub(pd.Series([-50,-50,50,50], index=['minx','miny','maxx','maxy']))