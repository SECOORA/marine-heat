# Purpose: Create a simple bar chart showing the depths at each station
#
# Date of Version 01: Nov. 03, 2025
#
# Author 01: Alexander Nickerson
#

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.ticker import MultipleLocator

# open station lists
stat_A = pd.read_csv(('Stats/Trends_Year.txt'),
                        header=0, sep="|", index_col=False)

folder = "Figs/Statistics/"

# create the folder only if necessary
if not os.path.exists(folder):
    os.makedirs(folder)
    
# my personal preferences for font
plt.rcParams["font.family"] = "serif"
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 12
res = 100

px, py = 800, 200

fig, ax = plt.subplots(figsize=(px/res, py/res),dpi=res)
plt.draw()

# axis labels; rotate the x-axis labels 90 degrees
ax.set_ylabel(r'Count')

# x-axis limits and ticks; rotate the x-axis labels 90 degrees
ax.set_xlim(-0.1,1.2)
ax.set_xticks(np.arange(-0.1,1.21,step=0.10))
ax.xaxis.set_minor_locator(MultipleLocator(5))
ax.set_xticklabels(np.arange(-0.1,1.21,step=0.10),rotation=90)
ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
ax.set_xlabel(r'Trend')
    
# y-axis limits and titles
ax.set_ylim(0,16)
ax.set_yticks(np.arange(0,16,step=5))
ax.yaxis.set_minor_locator(MultipleLocator(1))
ax.set_yticklabels(np.arange(0,16,step=5))
ax.set_ylabel(r'Count')
  
# plot title
ax.set_title(r'Number of Stations by Trend ($^{\circ}$C/dec)')

for i in range(10,31,10):
    Pt_A = ((stat_A["N_Mn"] >= i) & (stat_A["N_Mn"] < i + 10))
    sA = stat_A.loc[Pt_A,:].reset_index(drop=True)
    
    print(sA["Trend"].median()*10)
      
    # plot title
    ax.set_title(r'Number of Stations by Trend ($^{\circ}$C/dec)')
    
    # make bars
    count, bins, bars = ax.hist(np.array(sA["Trend"]*10),bins=np.arange(-0.3,1.5,step=0.05),
            color='r')
    
    # save file
    file2save = folder + "Counts_Trends_Year" + str(i) + ".png"
    fig.savefig(file2save,bbox_inches='tight',dpi=300)
    
    _ = [b.remove() for b in bars]
    
Pt_A = ((stat_A["N_Mn"] >= 10) & (stat_A["N_Mn"] < 100))
sA = stat_A.loc[Pt_A,:].reset_index(drop=True)

# make bars
ax.hist(np.array(sA["Trend"]*10),bins=np.arange(-0.3,1.5,step=0.05),
        color='r')

# save file
file2save = folder + "Counts_Trends_All.png"
fig.savefig(file2save,bbox_inches='tight',dpi=300)
