import geopandas as gpd
import pandas as pd
from geopandas.geoseries import *
from shapely import wkt
from shapely.geometry import box
import matplotlib.pyplot as plt
from functions import *

# converting row input of four min/max to rectangle vertices
def rectangulator (ip):
    rect = box(ip[0], ip[1], ip[2], ip[3])
    return rect

# this refines road within the 25m boundary box for futher analysis
def roadpicker(parkbound_row,roadboundlist,roadlist):
    boxminx = parkbound_row[0]
    boxminy = parkbound_row[1]
    boxmaxx = parkbound_row[2]
    boxmaxy = parkbound_row[3]
    # min of road smaller than max of park
    road_index = roadboundlist[roadboundlist['minx']<boxmaxx]
    road_index = road_index[road_index['miny']<boxmaxy]
    # max of road larger than min of park
    road_index = road_index[road_index['maxx']>boxminx]
    road_index = road_index[road_index['maxy']>boxminy]
    surrounded_road = roadlist[roadlist.index.isin(road_index.index)]
    return surrounded_road

# iterates roads within radus boundary of the park
def isinbound(parkroad_row_geom,park_rowi,width):
    parkgeom = park_rowi.geometry
    roadgeom = parkroad_row_geom
    return parkgeom.distance(roadgeom) <= width