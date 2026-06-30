# Purpose: Combine the two lists into one
#
# Date of Version 01: Mar. 04, 2026
#
# Author 01: Alexander Nickerson
#

import pandas as pd
    
# open lists of stations and remove the excess white space
stat_N = pd.read_csv('Docs/List_Download_NDBC.txt',
                        header=0, sep="|", index_col=False)
stat_E = pd.read_csv('Docs/List_Download_ERDDAP.txt',
                        header=0, sep="|", index_col=False)
                        
stat_N = stat_N.map(lambda x: x.strip() if isinstance(x, str) else x)
stat_E = stat_E.map(lambda x: x.strip() if isinstance(x, str) else x)

# combine the station listings and sort them
stat_all = pd.concat([stat_N, stat_E], ignore_index=True)
stat_all = stat_all.sort_values(by=["Type","Abr","Reg"]).reset_index(drop=True)

# prepare the columns and write them to a CSV file
stat_all["Reg"] = stat_all["Reg"].astype(str).str.rjust(40) + " "
stat_all["Type"] = " " +stat_all["Type"].str.ljust(5)
stat_all["Abr"] = " " +stat_all["Abr"].str.ljust(17)
stat_all["Lon"] = stat_all["Lon"].map("{:+9.3f}".format) + " "
stat_all["Lat"] = stat_all["Lat"].map("{:+9.3f}".format) + " "
stat_all["Org"] = " " + stat_all["Org"].str.replace("\"","").str.ljust(125)
stat_all["Name"] = " " + stat_all["Name"].astype(str)

stat_all.to_csv('Docs/List_Download_All.txt',index=False,sep="|")
