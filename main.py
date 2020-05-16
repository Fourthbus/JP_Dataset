import geopandas as gpd
import pandas as pd
from geopandas.geoseries import *
from shapely import wkt
from shapely.geometry import box
import matplotlib.pyplot as plt

# =============================================================================
# 
# just for fun stuff plotting
# plot = road.plot(column='I_C_R800',capstyle='round')
# fig = plot.get_figure()
# fig.savefig('output.svg')
# =============================================================================
# 
# fig, ax = plt.subplots()
# ax.set_aspect('equal')
# park_ext_rect.geometry.plot(ax=ax, color='grey')
# park.geometry.plot(ax=ax, color='green')
# plt.show()
# fig = ax.get_figure()
# fig.savefig('parkbox.svg')
# =============================================================================
# 
# fig, ax = plt.subplots()
# ax.set_aspect('equal')
# park.iloc[[1183]].geometry.plot(ax=ax, color='w' ,ec='green', lw=0.5)
# richmondroad.plot(ax=ax,column='I_C_R800',capstyle='round')
# plt.show()
# fig = ax.get_figure()
# fig.savefig('richmondrefine.svg')
# =============================================================================
#
# fig, ax = plt.subplots()
# ax.set_aspect('equal')
# park.iloc[[1183]].geometry.plot(ax=ax, color='w' ,ec='green', lw=0.5)
# alist.plot(ax=ax,column='I_C_R800',capstyle='round')
# plt.show()
# fig = ax.get_figure()
# fig.savefig('richmondrefine_r50.svg')
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
    
# load files
road = gpd.read_file("Road/London road link_subtracted_Segment_Map.shp")
park = gpd.read_file("GIGL/GiGL_OPS_filtered_CopyFeatur.shp")

roadsbound = road.geometry.bounds
parksbound = park.geometry.bounds

# extended parkbox by 25m
ext_bound     = 50
parksbound_ext = parksbound.add(pd.Series([-ext_bound,-ext_bound,ext_bound,ext_bound], index=['minx','miny','maxx','maxy']))

# make the boundary of each park back to a rectangle POLYGON
parks_ext_rect = pd.DataFrame(columns=['geometry'])
parks_ext_rect['geometry'] = parksbound_ext.apply(retangulator,axis=1)
# convert rectdata to GeoDataframe
parks_ext_rect = gpd.GeoDataFrame(parks_ext_rect, geometry='geometry')


# each row of the park extended boundary array
park_row = park.iloc[1183]
park_bound = parksbound_ext.iloc[1183].values.tolist()

# roads within the box
parkroad = roadpicker(park_bound,roadsbound,road)

# for each park it will create a
boundwidth = ext_bound

# roads within the radius
parkroad_r = parkroad[parkroad.geometry.apply(isinbound, park_row=parkrow, width=boundwidth)]

