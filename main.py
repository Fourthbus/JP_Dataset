import geopandas as gpd
import pandas as pd
from geopandas.geoseries import *
from shapely import wkt
from shapely.geometry import box
import matplotlib.pyplot as plt
from functions import *

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



    
# load files
road = gpd.read_file("Road/London road link_subtracted_Segment_Map.shp")
park = gpd.read_file("GIGL/GiGL_OPS_filtered_CopyFeatur.shp")

roadsbound = road.geometry.bounds
parksbound = park.geometry.bounds

# extended parkbox by 25m
ext_bound     = 25
parksbound_ext = parksbound.add(pd.Series([-ext_bound,-ext_bound,ext_bound,ext_bound], index=['minx','miny','maxx','maxy']))

# make the boundary of each park back to a rectangle POLYGON
parks_ext_rect = pd.DataFrame(columns=['geometry'])
parks_ext_rect['geometry'] = parksbound_ext.apply(rectangulator,axis=1)
# convert rectdata to GeoDataframe
parks_ext_rect = gpd.GeoDataFrame(parks_ext_rect, geometry='geometry')


ind = park.index
columnname = ['SiteName','Borough','I800','C800','IC800','Count','geometry']
output = pd.DataFrame(columns=columnname)
outputgdf = gpd.GeoDataFrame(output, geometry='geometry')

for i in (ind):
    nsegment = 0
    ic800 = 0
    i800  = 0
    c800  = 0
    
    # each row of the park extended boundary array
    park_row = park.iloc[i]
    park_bound = parksbound_ext.iloc[i].values.tolist()
    
    # roads within the box
    parkroad = roadpicker(park_bound,roadsbound,road)
    
    # for each park it will create a
    boundwidth = ext_bound
    
    # roads within the radius
    roads_near_park = gpd.GeoDataFrame(columns=parkroad.columns,geometry='geometry')
    roads_near_park = roads_near_park.append(parkroad[parkroad.geometry.apply(isinbound, park_rowi=park_row, width=boundwidth)])
    
    nsegment = roads_near_park.geometry.count()
    ic800 = roads_near_park['I_C_R800'].sum()
    i800  = roads_near_park['T1024_Ch_1'].sum()
    c800  = roads_near_park['T1024_In_1'].sum()
    
    # parkdat = {'SiteName': park_row['SiteName'],
    #            'Borough' : park_row['Borough'],
    #            'I800'    : i800,
    #            'C800'    : c800,
    #            'IC800'   : ic800,
    #            'Count'   : nsegment,
    #            'geometry': park_row['geometry']}
    
    parkdat = [[park_row['SiteName'], park_row['Borough'], i800, c800, ic800, nsegment, park_row['geometry']]]
    # expdf = pd.DataFrame(parkdat)
    expgdf = gpd.GeoDataFrame(parkdat, columns=columnname, index=[i], geometry='geometry')
    # print(expdf)
    output = output.append(expgdf)
    
    
