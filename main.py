import geopandas as gpd
import pandas as pd
from geopandas.geoseries import *
from shapely import wkt
from shapely.geometry import box

# converting row input of four min/max to rectangle vertices
def retangulator (ip):
    rect = box(ip[0], ip[1], ip[2], ip[3])
    return rect

# gigl = gpd.read_file("GIGL/GIGL_OPS_filtered.shp")
road = gpd.read_file("Road/London road link_subtracted_Segment_Map.shp")
park = gpd.read_file("GIGL/GiGL_OPS_filtered_CopyFeatur.shp")
# roadworked = gpd.read_file("Road2/London_Road_subtracted.shp")

# pt = wkt.loads('POINT(520000 172000)')
# poly = gigl2d[: 1].geometry[0]
# line = road[: 1].geometry[0]

roadbound = road.geometry.bounds
parkbound = park.geometry.bounds

parkbound_judge = parkbound.add(pd.Series([-25,-25,25,25], index=['minx','miny','maxx','maxy']))



# initialising rectdata
rectdata = pd.DataFrame(columns=['geometry'])
rectdata['geometry'] = parkbound_judge.apply(retangulator,axis=1)
# convert rectdata to GeoDataframe
rectdata = gpd.GeoDataFrame(rectdata, geometry='geometry')

def inthebox (roadboundrow,rectrow):
    rbminx = roadboundrow[0]
    rbminy = roadboundrow[1]
    rbmaxx = roadboundrow[2]
    rbmaxy = roadboundrow[3]
    reminx = rectrow[0]
    reminy = rectrow[1]
    remaxx = rectrow[2]
    remaxy = rectrow[3]
    if reminx < rbminx < remaxx or reminx < rbmaxx < remaxx:
        xin = True
    else:
        xin = False
    if reminy < rbminy < remaxy or reminy < rbmaxy < remaxy:
        yin = True
    else:
        yin = False
        
    

    
rbsample.apply(inthebox,axis=1)