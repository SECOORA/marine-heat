# Purpose: Make plots of the QC'd FACT data
#
# Date of Version 01: Nov. 05, 2025
#
# Author 01: Alexander Nickerson
#

import numpy as np
import pandas as pd
import xarray as xr
from datetime import date
import marineheatwaves as mhw
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
    
# open lists of stations and remove the excess white space
stat_all = pd.read_csv('Docs/List_Climo_All.txt',
                        header=0, sep="|", index_col=False)

stat_all = stat_all.map(lambda x: x.strip() if isinstance(x, str) else x)

stat_all = stat_all.loc[((stat_all["N_Yr"] > 10) &
                         (stat_all["N_Mn"] >  3)),:].reset_index(drop=True)

# full time index for empty arrays to store data
index_full = pd.date_range(
    start = np.datetime64('1973-01-01'),
    end   = np.datetime64('2026-12-31'),
    freq='D'
)

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
    (stat_all["Lon"] > -81.20) &
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
    # create empty arrays to store the data
    data_grd_dy = pd.DataFrame(data=np.nan,index=index_full,columns=stat_all["Reg"])
    data_raw_dy = pd.DataFrame(data=np.nan,index=index_full,columns=stat_all["Reg"])
    data_m1s_dy = pd.DataFrame(data=np.nan,index=index_full,columns=stat_all["Reg"])
    data_m2s_dy = pd.DataFrame(data=np.nan,index=index_full,columns=stat_all["Reg"])
    data_m3s_dy = pd.DataFrame(data=np.nan,index=index_full,columns=stat_all["Reg"])
    data_m4s_dy = pd.DataFrame(data=np.nan,index=index_full,columns=stat_all["Reg"])
    
    # get subset of stations
    stat_reg = stat_all.loc[Pts[reg],:].reset_index(drop=True)
    
    # loop through stations
    for i, stat in stat_reg.iterrows():
        # data file to open
        file_dy = "Data/" + stat["Type"] + "/Climo/" + stat["Reg"].strip() + "_Day.nc"
        
        # open the daily data
        ds_dy = xr.open_dataset(file_dy)
        df_dy = ds_dy.to_dataframe()
        df_mh = df_dy.reset_index()
        ds_dy.close()
                
        # set points without data as nan, which is essential for computing means
        data_grd_dy.loc[ df_dy.index, stat["Reg"]] = 0
        data_raw_dy.loc[ df_dy.index, stat["Reg"]] = 0
        data_m1s_dy.loc[ df_dy.index, stat["Reg"]] = 0
        data_m2s_dy.loc[ df_dy.index, stat["Reg"]] = 0
        data_m3s_dy.loc[ df_dy.index, stat["Reg"]] = 0
        data_m4s_dy.loc[ df_dy.index, stat["Reg"]] = 0
        
        # get the number of depths
        col = df_dy.columns[2:]
        
        # get the number of depths
        nd = len(col) 
        
        # the date_ord must be forcibly reset because it retains its value
        # and thereby breaks the mhw.detect() function.
        # Likewise, climatologyPeriod has to be forcibly reset because otherwise
        # python retains the value from the prior instance and considers the value
        # to be defined already
        date_ord = None
        date_np = df_mh["time"].dt.date.to_numpy()
        date_ord = np.fromiter((d.toordinal() for d in date_np), dtype=np.int64)
        clim_per = [date.fromordinal(date_ord[0]).year,
                    date.fromordinal(date_ord[-1]).year]
        
        # get the depth
        txt = col[0]
        col_ind = data_raw_dy.columns.get_loc(stat["Reg"])
        
        # you must make a copy because mhw permanently alters the input array
        tmp = df_dy[txt].to_numpy().copy()
        
        # find the MHWs
        mhw_all,clim_WR = mhw.detect(date_ord,tmp,climatologyPeriod=clim_per,pctile=90,windowHalfWidth=5)
        mhw_all  = pd.DataFrame.from_dict(mhw_all)
        
        # loop through all MHW events
        for d, m in mhw_all.iterrows():
            MC = m["category"]
            
            # find the actual dates of the start and end of the MHW
            D1 = df_mh.loc[m["index_start"],"time"]
            D2 = df_mh.loc[m["index_end"]  ,"time"]
            
            # get the corresponding points in the storage dataframes
            P1 = data_raw_dy.index.get_loc(D1)
            P2 = data_raw_dy.index.get_loc(D2)
            
            # generic MHW event tracking
            data_raw_dy.iloc[P1:P2,col_ind] = 1
            
            # categorical MHW event tracking
            if MC == "Moderate":
                data_grd_dy.iloc[P1:P2,col_ind] = 1
                data_m1s_dy.iloc[P1:P2,col_ind] = 1
            elif MC == "Strong":
                data_grd_dy.iloc[P1:P2,col_ind] = 2
                data_m2s_dy.iloc[P1:P2,col_ind] = 1
            elif MC == "Severe":
                data_grd_dy.iloc[P1:P2,col_ind] = 3
                data_m3s_dy.iloc[P1:P2,col_ind] = 1
            elif MC == "Extreme":
                data_grd_dy.iloc[P1:P2,col_ind] = 4
                data_m4s_dy.iloc[P1:P2,col_ind] = 1
         
    # get the annual sums and means of the MHW event trackings
    sums_raw = data_raw_dy.resample('YS').sum(min_count=1)
    sums_m1s = data_m1s_dy.resample('YS').sum(min_count=1)
    sums_m2s = data_m2s_dy.resample('YS').sum(min_count=1)
    sums_m3s = data_m3s_dy.resample('YS').sum(min_count=1)
    sums_m4s = data_m4s_dy.resample('YS').sum(min_count=1)
    
    # trim off the last year because that year is in progress
    sums_raw = sums_raw.head(-1)
    sums_m1s = sums_m1s.head(-1)
    sums_m2s = sums_m2s.head(-1)
    sums_m3s = sums_m3s.head(-1)
    sums_m4s = sums_m4s.head(-1)
       
    # get the annual means of the various variables
    sums_raw_avg = sums_raw.mean(axis=1)
    sums_m1s_avg = sums_m1s.mean(axis=1)
    sums_m2s_avg = sums_m2s.mean(axis=1)
    sums_m3s_avg = sums_m3s.mean(axis=1)
    sums_m4s_avg = sums_m4s.mean(axis=1)
       
    # force nan where pd.mean() turned them into 0's
    sums_raw_avg[sums_raw_avg == 0] = np.nan
    sums_m1s_avg[sums_m1s_avg == 0] = np.nan
    sums_m2s_avg[sums_m2s_avg == 0] = np.nan
    sums_m3s_avg[sums_m3s_avg == 0] = np.nan
    sums_m4s_avg[sums_m4s_avg == 0] = np.nan
       
    # get the time steps as years in a numpy array for easy plotting
    dates = sums_raw_avg.index.year
    
    # time ranges for plotting the median lines
    Y1 = np.datetime64('1975-01-01T00:00:00').astype('datetime64[s]')
    Y2 = np.datetime64('1995-01-01T00:00:00').astype('datetime64[s]')
    Y3 = np.datetime64('2015-01-01T00:00:00').astype('datetime64[s]')
    Y4 = np.datetime64('2025-01-01T00:00:00').astype('datetime64[s]')
       
    R1 = (sums_raw_avg.index >= Y1) & (sums_raw_avg.index < Y2)
    R2 = (sums_raw_avg.index >= Y2) & (sums_raw_avg.index < Y3)
    R3 = (sums_raw_avg.index >= Y3) & (sums_raw_avg.index < Y4)
       
    # my personal preferences for font
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman"]
    plt.rcParams["font.size"] = 12

    # create the plot window with certain dimensions
    res = 100
    px, py = 800, 325

    fig = plt.figure(figsize=(px/res, py/res),dpi=res)
    pos = [50/px,50/py,730/px,220/py]
    ax = fig.add_axes(pos)
    plt.draw()  
       
    # y-axis limits and ticks
    ax.set_xlim(1970,2026)
    ax.set_xticks(np.arange(1970,2026,step=5))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.set_ylim(0,60)
    ax.set_yticks(np.arange(0,61,step=10))
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    ax.tick_params(top=True, right=True, bottom=True, left=True)
    ax.grid()

    ax.set_xlabel('Date')
    ax.set_ylabel('Marine Heat Wave Days')
       
    ########################## SUMS - RAW
    # plot the data
    ax.plot([dates[0],dates[-1]],[sums_raw_avg.loc[R1].median(),
                                  sums_raw_avg.loc[R1].median()],'k-')
    ax.plot([dates[0],dates[-1]],[sums_raw_avg.loc[R2].median(),
                                  sums_raw_avg.loc[R2].median()],'k:')
    ax.plot([dates[0],dates[-1]],[sums_raw_avg.loc[R3].median(),
                                  sums_raw_avg.loc[R3].median()],'k--')
    
    # plot the categorical data   
    ck = '#000000'
    cb = '#1A1AFF'
    cg = '#1FFF35'
    cr = '#FF311F'
    cm = '#FF00FF'
       
    c0, = ax.plot(dates,sums_raw_avg,marker='.',c=ck,ms=12,ls='none')
    c1, = ax.plot(dates,sums_m1s_avg,marker='.',c=cb,ms=12,ls='none')
    c2, = ax.plot(dates,sums_m2s_avg,marker='.',c=cg,ms=12,ls='none')
    c3, = ax.plot(dates,sums_m3s_avg,marker='.',c=cr,ms=12,ls='none')
    c4, = ax.plot(dates,sums_m4s_avg,marker='.',c=cm,ms=12,ls='none')
    
    ax.legend([c0,c1,c2,c3,c4],
              ['All','Moderate','Strong','Severe','Extreme'],
              loc='upper left',
              fancybox=False,
              framealpha=1.0,
              edgecolor='k')
       
    # plot title
    fig.suptitle("Marine Heat Wave Events by Year for" +
                 " \n the " + place[reg])
       
    # create the name for the saved figure
    file2save = "Figs/Statistics/MHW_Events_" + reg + ".png"
       
    # save the figure
    fig.savefig(file2save, dpi=300)
       
    # remove the title
    fig.suptitle("")
       
    # remove the plot
    for line in ax.lines:
        line.remove()
       
    # close the figure to save memory
    plt.close(1)

