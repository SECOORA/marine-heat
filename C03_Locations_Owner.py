# Purpose: Create a simple map showing where the stations are found.
#
# Date of Version 01: Oct. 16, 2025
#
# Author 01: Alexander Nickerson
#

import numpy as np
import pandas as pd
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

for t in np.unique(stat_all["Abr"]):
    stat_own = stat_all.loc[stat_all["Abr"] == t,:]
    
    if len(stat_own) < 10:
        continue

    fig, ax = cm.map_C03(np.min(stat_own["Lon"])-0.2,
                         np.max(stat_own["Lon"])+0.2,
                         np.min(stat_own["Lat"])-0.2,
                         np.max(stat_own["Lat"])+0.2)

    ax.plot(stat_own["Lon"],stat_own["Lat"],'ro',markersize=1,mfc='r')

    # save the figure
    file2save = folder + "Locations_Owner_" + t + ".png"
    fig.savefig(file2save, dpi=300,bbox_inches='tight')

    for line in ax.lines:
        line.remove()
        
    plt.close()
