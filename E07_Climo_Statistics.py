# Purpose: Make a table of stations measuring data and having sufficient data
#          to compute annual means in any given year,
#
# Date of Version 01: Jun. 12, 2026
#
# Author 01: Alexander Nickerson
#

import pandas as pd
import os

# open lists of stations and remove the excess white space
stat_all = pd.read_csv('Docs/List_Climo_All.txt',
                        header=0, sep="|", index_col=False)

stat_all = stat_all.map(lambda x: x.strip() if isinstance(x, str) else x)

folder = "Stats/"
if not os.path.exists(folder):
    os.makedirs(folder)
    
years = [[ 0, 1],
         [ 1, 3],
         [ 3, 5],
         [ 6,11],
         [11,16],
         [16,21],
         [21,31],
         [31,41],
         [41,51],
         [51,99]]

years_list = [
    f"{'_'.join(f'{num:02d}' for num in sublist)}_Years"
    for sublist in years
]

data_yr = pd.DataFrame(data=None,index=years_list,columns=["Years","Means"])

for i, y in enumerate(years):
    Pt_Yr = ((stat_all["N_Yr"] >= y[0]) & (stat_all["N_Yr"] < y[1]))
    Pt_Mn = ((stat_all["N_Mn"] >= y[0]) & (stat_all["N_Mn"] < y[1]))
    
    data_yr.iloc[i,0] = sum(Pt_Yr)
    data_yr.iloc[i,1] = sum(Pt_Mn)

data_yr = data_yr.reset_index(drop=False)
data_yr.columns = ["Range","Years","Means"]

data_yr["Range"] = data_yr["Range"].str.rjust(11) + " "
data_yr["Years"] = data_yr["Years"].map("{:6.0f}".format) + " "
data_yr["Means"] = data_yr["Means"].map("{:6.0f}".format)

data_yr.columns = [("Range ").rjust(12),
                   (" Years ").rjust(6),
                   (" Means ").rjust(6)]


data_yr.to_csv('Stats/Climo_Years.txt',index=False,sep="|")