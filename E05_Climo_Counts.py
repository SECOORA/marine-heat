# Purpose: Create a simple bar chart showing the number of stations
#
# Date of Version 01: Oct. 15, 2025
#
# Author 01: Alexander Nickerson
#

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
    
# open lists of stations and remove the excess white space
stat_all = pd.read_csv('Docs/List_Climo_All.txt',
                        header=0, sep="|", index_col=False)

stat_all = stat_all.map(lambda x: x.strip() if isinstance(x, str) else x)

folder = "Figs/Statistics/"
if not os.path.exists(folder):
    os.makedirs(folder)

# count stations by number of years with calculated annual means
station = np.unique(stat_all["N_Mn"], return_counts=True)
ct = len(station[0])
data = np.concatenate((np.reshape(station[0],shape=(1,ct)),
                       np.reshape(station[1],shape=(1,ct)))).T

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
ax.set_xlim(-1,36)
ax.set_xticks(np.arange(0,36,step=5))
ax.set_xticklabels(np.arange(0,36,step=5),rotation=90)
   
# y-axis limits and ticks
ax.set_xlabel(r'Years') 
ax.set_ylabel(r'Count')
ax.set_yscale('log')
ax.set_ylim(0.9,500)
ax.set_yticks([1,10,100,500])
ax.set_yticklabels([1,10,100,500])

# plot title
ax.set_title("Number of Stations by Years with Mean Temperatures")

# plot data
for d in data:    
    x_box = [d[0]-0.25,d[0]+0.25,d[0]+0.25,d[0]-0.25,d[0]-0.25]
    y_box = [-20,-20,d[1],d[1],-20]
    ax.fill(x_box, y_box, "r")

file2save = folder + "Climo_Years.png"
fig.savefig(file2save,bbox_inches='tight',dpi=300)
    
# count stations by number of years with data
station = np.unique(stat_all["N_Yr"], return_counts=True)
ct = len(station[0])
data = np.concatenate((np.reshape(station[0],shape=(1,ct)),
                       np.reshape(station[1],shape=(1,ct)))).T

# my personal preferences for font
plt.rcParams["font.family"] = "serif"
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 12

# It's easier to just make a new window
# create the figure window
res = 100
px, py = 600, 235

fig = plt.figure(figsize=(px/res, py/res),dpi=res)
pos = [50/px,50/py,530/px,170/py]
ax = fig.add_axes(pos)
plt.draw()  

# x-axis limits and ticks
ax.set_xlim(-1,55)
ax.set_xticks(np.arange(0,55,step=5))
ax.set_xticklabels(np.arange(0,55,step=5),rotation=90)
    
# y-axis limits and ticks 
ax.set_xlabel(r'Years')
ax.set_ylabel(r'Count')
ax.set_yscale('log')
ax.set_ylim(0.9,500)
ax.set_yticks([1,10,100,500])
ax.set_yticklabels([1,10,100,500])
    
# plot title
ax.set_title("Number of Stations by Length of Time Series ")

# plot data
for d in data:
    x_box = [d[0]-0.25,d[0]+0.25,d[0]+0.25,d[0]-0.25,d[0]-0.25]
    y_box = [-20,-20,d[1],d[1],-20]
    ax.fill(x_box, y_box, "r")

file2save = folder + "Climo_Length.png"
fig.savefig(file2save,bbox_inches='tight',dpi=300)
