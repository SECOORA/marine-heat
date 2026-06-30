# Purpose: Create a simple map showing where the stations are found.
#
# Date of Version 01: Oct. 16, 2025
#
# Author 01: Alexander Nickerson
#

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import C03_Map as cm
    
# open lists of stations and remove the excess white space
stat_all = pd.read_csv('Docs/List_Download_All.txt',
                        header=0, sep="|", index_col=False)

stat_all = stat_all.map(lambda x: x.strip() if isinstance(x, str) else x)

folder = "Figs/Maps/"

# create the folder only if necessary
if not os.path.exists(folder):
    os.makedirs(folder)
# end if   
    
plt.rcParams["font.family"] = "serif"
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 12
plt.rcParams['figure.constrained_layout.use'] = True 

# set figure limits
fig, ax = cm.map_C03(np.floor( np.min(stat_all["Lon"]) ),
                     np.ceil(  np.max(stat_all["Lon"]) ),
                     np.floor( np.min(stat_all["Lat"]) ),
                     np.ceil(  np.max(stat_all["Lat"]) ))
    
# plot title
ax.set_title("Locations of All Stations")

# plot world map
world = gpd.read_file(
    "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
)
world.plot(ax=ax, color=[0.7,0.7,0.7], edgecolor='black')  # You can change 'skyblue' to any color

ax.plot(stat_all["Lon"],stat_all["Lat"],'ro',markersize=1,mfc='r')

# save the figure
file2save = folder + "Locations_All.png"
fig.savefig(file2save, dpi=300,bbox_inches='tight')

for line in ax.lines:
    line.remove()
    
lab = {"FACT": "FACT",
       "NDBC": "NDBC",
       "SWT":  "Other Temperature",
       "USF":  "USF-COMPS"}

for t in ["FACT","NDBC","SWT","USF"]:
    stat_typ = stat_all.loc[stat_all["Type"] == t,:]

    # set figure limits
    fig, ax = cm.map_C03(np.min(stat_typ["Lon"])-0.2,
                         np.max(stat_typ["Lon"])+0.2,
                         np.min(stat_typ["Lat"])-0.2,
                         np.max(stat_typ["Lat"])+0.2)
    
    ms = 1
    if (t == "FACT"):
        ms = 1
    elif (t == "USF"):
        ms = 5
    elif (t == "NDBC") or (t == "SWT"):
        ms = 3
    ax.plot(stat_typ["Lon"],stat_typ["Lat"],'ro',markersize=ms,mfc='r')
        
    # plot title
    ax.set_title("Locations of " + lab[t] + " Stations")

    # save the figure
    file2save = folder + "Locations_Type_" + t + ".png"
    fig.savefig(file2save, dpi=300,bbox_inches='tight')

    for line in ax.lines:
        line.remove()
        
    plt.close()
