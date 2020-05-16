import geopandas as gpd
import pandas as pd
from geopandas.geoseries import *
from shapely import wkt
from shapely.geometry import box
import matplotlib.pyplot as plt

# =============================================================================
# just for fun stuff pl
# =============================================================================






# converting row input of four min/max to rectangle vertices
def retangulator (ip):
    rect = box(ip[0], ip[1], ip[2], ip[3])
    return rect

# this refines road within the 25m boundary box for futher analysis
def roadpicker(parkbound_row,roadboundlist,roadlist):
    boxminx = parkbound_row[0]
    boxminy = parkbound_row[1]
    boxmaxx = parkbound_row[2]
    boxmaxy = parkbound_row[3]
    # min of road smaller than max of park
    road_index = roadbound[roadbound['minx']<boxmaxx]
    road_index = road_index[road_index['miny']<boxmaxy]
    # max of road larger than min of park
    road_index = road_index[road_index['maxx']>boxminx]
    road_index = road_index[road_index['maxy']>boxminy]
    surrounded_road = roadlist[roadlist.index.isin(road_index.index)]
    return surrounded_road
    

# gigl = gpd.read_file("GIGL/GIGL_OPS_filtered.shp")
road = gpd.read_file("Road/London road link_subtracted_Segment_Map.shp")
park = gpd.read_file("GIGL/GiGL_OPS_filtered_CopyFeatur.shp")
# roadworked = gpd.read_file("Road2/London_Road_subtracted.shp")

# pt = wkt.loads('POINT(520000 172000)')
# poly = gigl2d[: 1].geometry[0]
# line = road[: 1].geometry[0]

roadbound = road.geometry.bounds
parkbound = park.geometry.bounds

# extended parkbox by 25m
ext_bound     = 25
parkbound_ext = parkbound.add(pd.Series([-ext_bound,-ext_bound,ext_bound,ext_bound], index=['minx','miny','maxx','maxy']))



# initialising rectdata
park_ext_rect = pd.DataFrame(columns=['geometry'])
park_ext_rect['geometry'] = parkbound_ext.apply(retangulator,axis=1)
# convert rectdata to GeoDataframe
park_ext_rect = gpd.GeoDataFrame(rectdata, geometry='geometry')

# def inthebox (roadboundrow,rectrow):
#     rbminx = roadboundrow[0]
#     rbminy = roadboundrow[1]
#     rbmaxx = roadboundrow[2]
#     rbmaxy = roadboundrow[3]
#     reminx = rectrow[0]
#     reminy = rectrow[1]
#     remaxx = rectrow[2]
#     remaxy = rectrow[3]
#     if reminx < rbminx < remaxx or reminx < rbmaxx < remaxx:
#         xin = True
#     else:
#         xin = False
#     if reminy < rbminy < remaxy or reminy < rbmaxy < remaxy:
#         yin = True
#     else:
#         yin = False
#     if xin and yin:
#         return True
#     else:
#         return False
 

# each row of the park extended boundary array   
richmond = parkbound_ext.iloc [[1183]].values[0].tolist()

rochmondroad = roadpicker(richmond,roadbound,road)

fig, ax = plt.subplots()

