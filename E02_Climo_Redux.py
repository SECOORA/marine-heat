# Purpose: Combine the two lists into one
#
# Date of Version 01: Mar. 04, 2026
#
# Author 01: Alexander Nickerson
#

import pandas as pd

# open lists of stations and remove the excess white space
stat_all = pd.read_csv('Docs/List_Climo_All.txt',
                        header=0, sep="|", index_col=False)

stat_all = stat_all.map(lambda x: x.strip() if isinstance(x, str) else x)

# convert important variable to integer
stat_all["N_Mn"] = stat_all["N_Mn"].astype(int)

# collect subset of array
stat_reg = stat_all.loc[stat_all["N_Mn"] >= 3,:].copy()

# return column to string
stat_reg["N_Mn"] = " " + stat_reg["N_Mn"].map("{:2d}".format)

# save data
stat_reg.to_csv('Docs/List_Climo_Redux.txt',index=False,sep="|")
