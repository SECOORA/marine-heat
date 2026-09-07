# Purpose: Combine the lists into one
#
# Date of Version 01: May  23, 2025
# Date of Version 02: Sep. 07, 2026
#
# Author 01: Alexander Nickerson
# Author 02: Alexander Nickerson
#
# Version 02 debugs errors that were present in the first version.
#

import os
import pandas as pd
import numpy as np
    
# open list of stations and remove the excess white space
stat_all = pd.read_csv('Docs/List_Redux_NDBC.txt',
                        header=0, sep="|", index_col=False)

stat_all = stat_all.map(lambda x: x.strip() if isinstance(x, str) else x)

# sort the columns
stat_all = stat_all.sort_values(by=['Org','Reg']).reset_index(drop=True)

# get the list of files
folder = "Data/NDBC/L00D/"
file_all = sorted([f for f in os.listdir(folder)])

# convert the list to a dataframe
file_all = pd.DataFrame(file_all, columns=["Buoy"])

# force convert the dataframe to a numeric dataframe so that Apple's "._" and
#       "DS_Store" files get converted to NaN
file_all["Buoy"] = pd.to_numeric(file_all["Buoy"], errors="coerce")

# ID the NaN's, remove them from the data frame, and convert to integer
good = ~np.isnan(file_all["Buoy"])
file_all = file_all.loc[good,:].reset_index(drop=True)
file_all["Buoy"] = file_all["Buoy"].astype("int64")

# check for stations that actually downloaded data and keep those only
is_down = stat_all["Reg"].isin(file_all["Buoy"])
stat_all = stat_all.loc[is_down == True].reset_index(drop=True)

# prepare the columns and write them to a CSV file
stat_all["Reg"] = stat_all["Reg"].astype(str).str.rjust(40) + " "
stat_all["Type"] = stat_all["Type"].str.ljust(5)
stat_all["Abr"] = stat_all["Abr"].str.ljust(17)
stat_all["Lon"] = stat_all["Lon"].map("{:+9.3f}".format) + " "
stat_all["Lat"] = stat_all["Lat"].map("{:+9.3f}".format) + " "
stat_all["Org"] = stat_all["Org"].str.replace("\"","").str.ljust(125)
stat_all["Name"] = stat_all["Reg"].astype(str)

stat_all.to_csv('Docs/List_Download_NDBC.txt',index=False,sep="|")
