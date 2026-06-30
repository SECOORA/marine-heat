# Purpose: Create a simple bar chart showing the number of stations that have
#          measurements in any given year
#
# Date of Version 01: Jun. 12, 2026
#
# Author 01: Alexander Nickerson
#

import numpy as np
import xarray as xr
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
    
# open lists of stations and remove the excess white space
stat_all = pd.read_csv('Docs/List_Climo_All.txt',
                        header=0, sep="|", index_col=False)

stat_all = stat_all.map(lambda x: x.strip() if isinstance(x, str) else x)

folder = "Figs/Statistics/"
if not os.path.exists(folder):
    os.makedirs(folder)
    
# counter for years of data
data = {year: 0 for year in range(1970, 2026)}

# loop through stations
for i, stat in stat_all.iterrows():
    file2open = ("Data/" + stat["Type"] + "/Climo/" + 
                       str(stat["Reg"]) + "_Year.nc")
    
    # open the file
    ds = xr.open_dataset(file2open)
    df = ds.to_dataframe()
    df = df.reset_index()
    ds.close()
    
    df["dy"] = np.nansum(df.iloc[:,2:],1)
    df["time"] = df["time"].dt.year
    
    yrs = df.loc[df["dy"]>0,"time"].tolist()
    
    for y in yrs:
        data[y] += 1
    
# my personal preferences for font
plt.rcParams["font.family"] = "serif"
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 12

# create the figure window
res = 100
px, py = 600, 235

fig = plt.figure(figsize=(px/res, py/res),dpi=res)
pos = [50/px,50/py,530/px,170/py]
ax = fig.add_axes(pos)
plt.draw()  

# x-axis limits and ticks
ax.set_xlim(1975,2026)
ax.set_xticks(np.arange(1975,2026,step=5))
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.set_xticklabels(np.arange(1975,2026,step=5),rotation=90)
   
# y-axis limits and ticks
ax.set_xlabel(r'Year') 
ax.set_ylabel(r'Count')
ax.set_yscale('log')
ax.set_ylim(0.9,500)
ax.set_yticks([1,10,100,500])
ax.set_yticklabels([1,10,100,500])

# plot title
ax.set_title("Years by Number of Stations with Mean Temperatures" +
             " \n for the entire SECOORA region")

# plot data
for d in data:    
    x_box = [d-0.25,d+0.25,d+0.25,d-0.25,d-0.25]
    y_box = [-20,-20,data[d],data[d],-20]
    ax.fill(x_box, y_box, "r")
   
# line demarcating 30 years of data 
ax.plot([29.5,29.5],[-100000,100000],'k-')

file2save = folder + "Data_Years_All.png"
fig.savefig(file2save,bbox_inches='tight',dpi=300)

# establish empty dataframe to hold empty logical arrays
Pts = pd.DataFrame(data=None,index=stat_all.index,
                   columns=["WFS","FLA","GSC","NC","ENP"])

# get logical arrays for each region
Pts["WFS"] = (
    (stat_all["Lat"] >  25.00) &
    (stat_all["Lat"] <  30.41) &
    (stat_all["Lon"] > -87.52) &
    (stat_all["Lon"] < -81.66)
)

Pts["FLA"] = (
    (stat_all["Lat"] >  25.42) &
    (stat_all["Lat"] <  30.71) &
    (stat_all["Lon"] > -81.66) &
    (stat_all["Lon"] < -80.00)
)

Pts["GSC"] = (
    (stat_all["Lat"] >  30.71) &
    (stat_all["Lat"] <  36.50) &
    (stat_all["Lon"] > -81.14) &
    (stat_all["Lon"] < -78.57)
)

Pts["NC"] = (
    (stat_all["Lat"] >  30.71) &
    (stat_all["Lat"] <  36.50) &
    (stat_all["Lon"] > -78.57) &
    (stat_all["Lon"] < -74.82)
)

Pts["ENP"] = (
    (~Pts["WFS"]) &
    (~Pts["FLA"]) &
    (~Pts["GSC"]) &
    (~Pts["NC"]) &
    (stat_all["Lon"] < -80.20)
)

place = {"ENP": "Everglades and Florida Keys",
         "FLA": "Florida Atlantic Waters",
         "GSC": "Georgia and South Carolina Atlantic Waters",
         "NC" : "North Carolina Atlantic Waters",
         "WFS": "West Florida Shelf"}

# loop through different regions
for reg in ["WFS","FLA","GSC","NC","ENP"]:
    # get subset of stations
    stat_reg = stat_all.loc[Pts[reg],:].reset_index(drop=True)
    
    # counter for years of data
    data = {year: 0 for year in range(1970, 2026)}

    # loop through stations
    for i, stat in stat_reg.iterrows():
        file2open = ("Data/" + stat["Type"] + "/Climo/" + 
                           str(stat["Reg"]) + "_Year.nc")
        
        # open the file
        ds = xr.open_dataset(file2open)
        df = ds.to_dataframe()
        df = df.reset_index()
        ds.close()
        
        df["dy"] = np.nansum(df.iloc[:,2:],1)
        df["time"] = df["time"].dt.year
        
        yrs = df.loc[df["dy"]>0,"time"].tolist()
        
        for y in yrs:
            data[y] += 1
        
    # my personal preferences for font
    plt.rcParams["font.family"] = "serif"
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['font.size'] = 12

    # create the figure window
    res = 100
    px, py = 600, 235

    fig = plt.figure(figsize=(px/res, py/res),dpi=res)
    pos = [50/px,50/py,530/px,170/py]
    ax = fig.add_axes(pos)
    plt.draw()  

    # x-axis limits and ticks
    ax.set_xlim(1975,2026)
    ax.set_xticks(np.arange(1975,2026,step=5))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.set_xticklabels(np.arange(1975,2026,step=5),rotation=90)
       
    # y-axis limits and ticks
    ax.set_xlabel(r'Year') 
    ax.set_ylabel(r'Count')
    ax.set_yscale('log')
    ax.set_ylim(0.9,500)
    ax.set_yticks([1,10,100,500])
    ax.set_yticklabels([1,10,100,500])

    # plot title
    ax.set_title("Years by Number of Stations with Mean Temperatures" +
                 " \n for the " + place[reg])

    # plot data
    for d in data:    
        x_box = [d-0.25,d+0.25,d+0.25,d-0.25,d-0.25]
        y_box = [-20,-20,data[d],data[d],-20]
        ax.fill(x_box, y_box, "r")
        
    # line demarcating 30 years of data
    ax.plot([29.5,29.5],[-100000,100000],'k-')

    file2save = folder + "Data_Years_" + reg + ".png"
    fig.savefig(file2save,bbox_inches='tight',dpi=300)
