#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np
import matplotlib.collections
from scipy.interpolate import interp1d
sns.set()
from results import load
from matplotlib.lines import Line2D

from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
from mpl_toolkits.axes_grid1.colorbar import colorbar

style = None
heatmap_cache = None
hmcmp = None

def plotWorkload(ax,data,label="Target Workload",interval=1000):
    data["RStart_1s"] = round(data["RStart"]/interval)
    #lats = data.groupby(["RStart_1s"])['RId'].count().reset_index(name="workload")
    lats = data.groupby(["RStart_1s"])['RId'].count()
    #sns.lineplot(x="RStart_1s", y='workload', data=lats, color="gray",label="Target Workload",ax=ax)
    lats.ewm(span = 4).mean().plot(color="gray", label =label,ax=ax)
    
def lighten_color(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import colorsys
    h = color.lstrip('#')
    
    c = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    c = map(lambda x:min(x+10,255),c)
    c = map(lambda x:hex(x)[2:],c)
    return "#{}{}{}".format(*c)

def plotLatColdWarm(ax,all,provider,workload,style,lat="DLat",title=None):
    if title is None:
        ax.set_title("{} {}".format(style[provider]["name"],style["Names"][lat]))
    else:
        ax.set_title(title)
    data = all[(all["Provider"] == provider) & (all["WL"] == workload)]
    #data = data[data["DLat"].notna()]
    #data = data[data["RCode"] != 429] #filters filed requests e.g. azure
    #data = data[data["Phase"].isin(["p1","p2"])]

    data = data.replace({'CNew': "New"}, {'CNew': 'Cold'})
    data = data.replace({'CNew': "Reused"}, {'CNew': 'Warm'})
    data = data.rename(columns={"CNew":"Type"})
    sns.violinplot(x='Phase', y=lat,hue="Type", data=data,  scale='count',
                   cut=0,ax=ax,  inner='quartile',split=True,bw='scott',
                   scale_hue=True,palette=style["CNew"])

    #ax.set_yscale('log')

    ax.set_xlabel("Phases")
    ax.set_ylabel(r"Latency [s]")
    #ax.set_ylim([0,20])
    #highlight phases

    #ax.set_xticklabels(["p0","p1","p2","none"])

    delta = 0.02
    delta = 0.02
    inner = None
    #code for gap between violin halves, from stackoverflow.com/questions/43357274/
    for ii, item in enumerate(ax.collections):
    # axis contains PolyCollections and PathCollections
        if isinstance(item, matplotlib.collections.PolyCollection):
        # get path
            path, = item.get_paths()
            vertices = path.vertices

        # shift x-coordinates of path
            if not inner:
                if ii % 2: # -> to right
                    vertices[:,0] += delta
                else: # -> to left
                    vertices[:,0] -= delta
            else: # inner='box' adds another type of PollyCollection
                if ii % 3 == 0:
                    vertices[:,0] -= delta
                elif ii % 3 == 1:
                    vertices[:,0] += delta
                else: # ii % 3 = 2
                    pass

def costPerSecond(ax,all,workload,style,providers=["aws","azure","ibm","gcf"],title=None):
    
    data = all[(all["WL"] == workload)&(all["Provider"].isin(providers))]
    #plot
    data = data[data["RLat"].notna()]
    data = data[data["RCode"] != 429] #filters filed requests e.g. azure
    data = data[data["Phase"].isin(["p1","p2"])]
    
    data = data.replace({'Phase': "p1"}, {'Phase': style["Names"]["p1"]})
    data = data.replace({'Phase': "p2"}, {'Phase': style["Names"]["p2"]})
    
    sns.violinplot(x='Provider', y='ECost',hue="Phase", data=data,  inner='quartile',split=True,
                  palette=style["Phases"])


    # ax.set_xlim([0,300])
    ax.set_xlabel("Phases")
    ax.set_ylabel(r"Cost [$\mu$\$]")
    ax.set_ylim([0,600])
    ax.xaxis.set_ticklabels(map(lambda x:style[x.get_text()]["name"],ax.xaxis.get_ticklabels()))
    ax.grid(False)
    #title
    if title is None:
        ax.set_title("{} - Cost per Request".format(workload))
    else:
        ax.set_title(title)

def plotHeatmap(ax,all,provider,workload,style,selector="HId",cutoff=0.5,xlim=[0,300],title=None,vmax=None,cmap=sns.cubehelix_palette(8),draw_first=True,legend=True,show_cba=True,heatmap_cache={}):
    #filter data
    data = all[(all['Provider'] == provider) & (all["WL"] == workload)]
    data = data[["EStart","EEnd",selector,"RId"]].copy()
    #remove NAN
    data = data[data["EStart"].notna()]
    data = data.reset_index()
    #second buckets
    data["EStart"] = round(data["EStart"]/1000)
    data["EEnd"] = round(data["EEnd"]/1000)

    #remove lower 20%
    X = data.groupby(selector)["RId"].count().reset_index(name="c")
    X = X[X["c"] > X["c"].quantile(cutoff)]
    
    #small note, we compress the datas x-axis by to otherwiese the plot gets to wide
    
    heatmap = None
    firstStart = None
    cache_key = "{}-{}{}-{}{}".format(selector,cutoff,str(xlim),provider,workload)
    if cache_key in heatmap_cache:
        heatmap = heatmap_cache[cache_key][0]
        firstStart = heatmap_cache[cache_key][1]
    else:
        HIdEStart = {}
        X = round(data.groupby(selector)["EStart"].min()/2)
        for hid in data[selector].unique():
            if hid in X.index:
                HIdEStart[hid] = max(0,int(X.loc[hid])-1)

        HIdIndex = {}
        idx = 0
        for hid in sorted(HIdEStart.items(), key=lambda s:s[1]):
            HIdIndex[hid[0]] = idx
            idx+=1


        #create first-start marker map
        firstStart = np.zeros((len(HIdIndex),round(xlim[1]/2)))
        for hid in HIdIndex.keys():
            if hid in X.index:
                idx = min(max(0,int(X.loc[hid])-1),firstStart.shape[1]-1)
                firstStart[HIdIndex[hid],idx] = 1

        #create heatmap by counting each invocation from EStart to EEnd
        heatmap = np.zeros((len(HIdIndex),round(xlim[1]/2)))
        for i in range(1,len(data)):
            x = data.loc[i,[selector,"EStart","EEnd"]]
            if x[selector] in HIdIndex.keys():
                #lets not talk about the following hack ;)
                for j in np.arange(x["EStart"],min(xlim[1],x["EEnd"]),2,dtype=int):

                    heatmap[HIdIndex[x[selector]],j>>1] +=1
            
        heatmap_cache[cache_key] = (heatmap,firstStart)
    if len(heatmap) > 0:
        sns.heatmap(heatmap,ax=ax,cmap=cmap,linewidths=0,cbar=False,vmax=vmax)
    if draw_first:
        highlight=[(1,1,1,0),(0,0,1,1)]
        sns.heatmap(firstStart,ax=ax,cmap=highlight,linewidths=0,cbar=False,vmin=0,vmax=1)
    if show_cba:
        ax_divider = make_axes_locatable(ax)
        # define size and padding of axes for colorbar
        cax = ax_divider.append_axes('right', size = '2.5%', pad = '1%')
        # make colorbar for heatmap. 
        # Heatmap returns an axes obj but you need to get a mappable obj (get_children)
        colorbar(ax.get_children()[0], cax = cax, orientation = 'vertical')
        # locate colorbar ticks
        cax.xaxis.set_ticks_position('top')
    ax.set_yticklabels([""])
    ax.set_xticks(ticks=[15,45,115])
    
    xticks = list(np.arange(0,round(xlim[1]/2)+1,30,dtype=int))
    #if not(round(xlim[1]/2) in xticks):
    xticks.append(round(xlim[1]/2))
    xticks.append(30)
    xticks.append(60)
    xticks = list(set(xticks))
    
    ax.set_xticks(ticks=xticks,minor=True)
    ax.set_xticklabels(map(lambda x:style["Names"][x],["p0","p1","p2"]),rotation='horizontal')
    ax.set_xticklabels(map(lambda x:str(x*2),ax.get_xticks(minor=True)),minor=True)
    ax.tick_params(axis='x', which='major', pad=15)
    if title is None:
        ax.set_title("{} [{}] - Parallel Requests per {} per Second".format(style[provider]["name"],workload,style["Names"][selector]))
    else:
        ax.set_title(title)
    ax.set_ylabel("Parallel Executions [#]")
    ax.set_xlabel("Elapsed Time [s]")
    
    ax.axvline(30,alpha=0.6,color="black")
    ax.axvline(60,alpha=0.6,color="black")
    if draw_first and legend:
        legendShapes = [Line2D([0], [0], marker='|', lw=0,color='blue',markerfacecolor='blue', markersize=10)]
        legendNames = ["First Occurrence"]
        ax.legend(legendShapes, legendNames,fancybox=True, shadow=True,facecolor='white')

def plotFailedRequestPerSecond(ax,data,provider,workload,style,plot_target=True,label=None,title=None,no_legend=False):
    data = data[(data['Provider'] == provider) & (data["WL"] == workload)]
    data = data.copy()
    if plot_target:
        plotWorkload(ax,data)
        
    data["RStart_1s"] = round(data["RStart"]/1000)
    #sum up cost
    data = data.groupby(["RStart_1s"])["RFailed"].sum().reset_index(name="RFailed")
    if label == None:
        label = "{}".format(style[provider]["name"])
    
    data = data[data["RFailed"] > 0]
    ax.scatter(x="RStart_1s", marker="+",y='RFailed', data=data, color="indianred",label=label,s=40)
    ax.set_xlim([0,300])
    ax.set_xlabel("time [s]")
    ax.set_ylabel(r"failed requests [#]")

    #highlight phases
    ax.axvline(60,alpha=0.7,color="black")
    ax.axvline(120,alpha=0.7,color="black")
    for i in range(0,300,20):
        ax.axvline(i,alpha=0.2,color="black")
    
    ax.grid(False)
    ax.set_xticks(ticks=[30,90,210])
    ax.set_xticks(ticks=range(0,300,20),minor=True)
    ax.set_xticklabels(map(lambda x:style["Names"][x],["p0","p1","p2"]))
    ax.set_xticklabels(range(0,300,20),minor=True)
    ax.tick_params(axis='both', which='major', pad=15)
    if title is True:
        ax.set_title("{} - Failed Request per Second".format(style[provider]["name"]))
    else:
        ax.set_title(title)
        
    if no_legend:
        ax.legend([])
    #title

def q(x,name):
    def _q(n):
        return np.percentile(n,x)
    _q.__name__ = name
    return _q

def prepLatData(data,provider,workload,quantile_bar=10):
    X = data[(data["Provider"] == provider) & (data["WL"] == workload)]
    X = X[["RLat","ELat","DLat","BLat","EStart","Phase"]]
    X["EStart"] = round(data["EStart"]/1000)
    X = X.groupby("EStart")[["RLat","ELat","DLat","BLat"]].agg([np.median,np.max,np.min,np.mean,q(quantile_bar,"pa"),q(100-quantile_bar,"pb")])
    new_index = pd.Index(np.arange(0,301,1), name="EStart")
    X = X.reindex(new_index)
    return X

def plotLineWithErrorBar(ax,data,color="lightblue",label=None,plot_quantile=False):
    ax.plot(data["median"],label=label,color=color,zorder=2)
    if plot_quantile:
        ax.plot(data["pa"],linestyle=":",color=color,alpha=0.65,zorder=3)
        ax.plot(data["pb"],linestyle=":",color=color,alpha=0.65,zorder=3)
    ax.fill_between(data.index,data["amax"],data["amin"],alpha=0.4,color=color,zorder=1)

def plotLatOverTime(ax,all,provider,workload,style,lat="DLat",title=None,label=None,no_labels=False,quantile_bar=10):
    data = prepLatData(all,provider,workload,quantile_bar)[lat]
    
    if label is None:
        label = "Median {0}".format(style["Names"][lat])
        

    plotLineWithErrorBar(ax,data,label=label,color=style["Lats"][lat])
    if not no_labels:
        ax.set_ylabel("{} in [s]".format(style["Names"][lat]))
        ax.set_xlabel("Time [s]")
        if title is None:
            ax.set_title("{} [{}] {} over Time".format(style[provider]["name"],workload,style["Names"][lat]))
        else:
            ax.set_title(title)
        ax.legend()
    else:
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.legend([])

def plotClientSideOverview(ax,data,provider,workload,style,title=False,legend=True,
                           ylim=[0,30],xlim=None,quantile_bar=10,plot_quantile=False,
                          with_thruput=False):
    lats = prepLatData(data,provider,workload,quantile_bar)[["ELat","RLat"]]
    ax2 = ax.twinx()
    plotLineWithErrorBar(ax2,lats["ELat"],style["Lats"]["ELat"],style["Names"]["ELat"])
    plotLineWithErrorBar(ax2,lats["RLat"],style["Lats"]["RLat"],style["Names"]["RLat"],plot_quantile=plot_quantile)
    ax2.set_ylabel(r"Latency [s]")
    ax2.grid(False)
    ax2.set_ylim(ylim)
    
    
    plotFailedRequestPerSecond(ax,data,provider,workload,style,label="Failed Requests",no_legend=True,title=None)
    
    if with_thruput:
        thruputPerSecondSimple(ax,data,provider,workload,style)
        
    if xlim is None:
        xlim = [0,300]
    
    ax.set_xlim(xlim)
    ax.set_xlabel("Elapsed Time [s]")
    ax.set_ylabel(r"Requests [#]")

    #highlight phases
    ax.axvline(60,alpha=0.7,color="black")
    ax.axvline(120,alpha=0.7,color="black")
    for i in range(0,xlim[1],20):
        ax.axvline(i,alpha=0.1,color="black")

    ax.grid(False)
    ax.set_xticks(ticks=[30,90,210])
    ax.set_xticks(ticks=range(0,xlim[1]+1,20),minor=True)
    ax.set_xticklabels(map(lambda x:style["Names"][x],["p0","p1","p2"]),minor=False)
    ax.set_xticklabels(range(0,xlim[1]+1,20),minor=True)
    ax.tick_params(axis='both', which='major', pad=15)
    if legend:
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines + lines2, labels + labels2,loc='center left', bbox_to_anchor=(1.15, 0.5),
                  ncol=1, fancybox=True, shadow=True)
    else:
        ax.get_legend().remove()
    
    if title is None:
        ax.set_title("{} [{}] Client-side Qualtites".format(style[provider]["name"],workload))
    else:
        ax.set_title(title)
        
    return ax,ax2

def thruputPerSecondSimple(ax,all,provider,workload,style,filter_failed=False):
    data = all.copy()
    data = data[(data['Provider'] == provider) & (data["WL"] == workload)]
    if filter_failed:
        data = data[data["RFailed"] == False]
        
    data["REnd_1s"] = round(data["REnd"]/1000)
    data = data.groupby(["REnd_1s"])["RId"].count().reset_index(name="throughput")
    ax.scatter(x="REnd_1s",y="throughput",marker="o",data=data,
               label="Throughput",c=style[provider]["color"],s=12)
    
def thruputPerSecond(ax,all,provider,workload,style,filter_failed=False,with_failed=True,with_dlat=True,title=None,xlim=[0,300],ylims=None):
    data = all[(all['Provider'] == provider) & (all["WL"] == workload)]
    data = data.copy()
    
    if with_failed:
        plotFailedRequestPerSecond(ax,data,provider,workload,style,False,
                                   "Failed Requests",no_legend=True)
        

    if filter_failed:
        data = data[data["RFailed"] == False]
        
    data["REnd_1s"] = round(data["REnd"]/1000)
    plotWorkload(ax,data)
    #goup by second
    data = data.groupby(["REnd_1s","CNew"])["RId"].count().reset_index(name="throughput")
    #plot
    ax.scatter(x="REnd_1s",y="throughput",marker="o",data=data[data["CNew"] == "Reused"],
               label="Throughput (Warm)",c=style["CNew"]["Reused"],s=12)
    ax.scatter(x="REnd_1s",y="throughput",marker="s",data=data[data["CNew"] == "New"],
               label="Throughput (Cold)",c=style["CNew"]["New"],
               alpha=0.8,s=12)
    
    ax.set_xlim([0,300])
    ax.set_xlabel("Time [s]")
    ax.set_ylabel(r"Request [#]")
    ax.set_ylim([0,180])
    
    #highlight phases
    ax.axvline(60,alpha=0.7,color="black")
    ax.axvline(120,alpha=0.7,color="black")
    for i in range(0,300,20):
        ax.axvline(i,alpha=0.1,color="black")
    
    ax.grid(False)
    ax.set_xticks(ticks=[30,90,210])
    ax.set_xticks(ticks=range(0,301,20),minor=True)
    ax.set_xticklabels(map(lambda x:style["Names"][x],["p0","p1","p2"]),minor=False)
    ax.set_xticklabels(ax.get_xticks(minor=True),minor=True)
    ax.tick_params(axis='both', which='major', pad=15)
    #ax.set_xticks(ticks=ylim,minor=True)
    ax2 = ax.twinx()
    if with_dlat:
        data = all[(all['Provider'] == provider) & (all["WL"] == workload)]
        data = data[["RLat","DLat","EStart","Phase"]]
        data["EStart"] = round(data["EStart"]/1000)
        data =data.groupby("EStart")[["RLat","DLat"]].agg([np.median,np.max,np.min,np.mean])
        plotLineWithErrorBar(ax2,data["DLat"],style["Lats"]["DLat"],style["Names"]["DLat"])
        #setting second y-axis limits
        if ylims is not None:
            ax2.set_ylim(ylims[provider][workload])
        ax2.set_ylabel("{} [s]".format(style["Names"]["DLat"]))
        ax2.grid(False,"both")
    
    #title
    if title is None:
        ax.set_title("{} [{}] - Throughput per Second".format(style[provider]["name"],workload))
    else:
        ax.set_title(title)
        
    ax.set_xlim(xlim)
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.get_legend().remove()
    leg = ax2.legend(lines + lines2, labels + labels2,loc='upper left',
                  ncol=1, fancybox=True, shadow=True,facecolor="white")
    
def client_view_legend(ax,style):
    legendShapes = [
    Line2D([0], [0], color="gray", lw=2),
    Line2D([0], [0], marker='+', lw=0,color='indianred',markerfacecolor='indianred', markersize=10),
    Line2D([0], [0], color=style["Lats"]["RLat"], lw=2),
    Line2D([0], [0], color=style["Lats"]["ELat"], lw=2),
    ]
    legendNames = ["trps","RFailed","RLat","ELat",]
    ax.legend(legendShapes, legendNames,loc="upper left",fancybox=True, shadow=True)

def provider_view_legend(ax,style):
    legendShapes = [
    Line2D([0], [0], marker='|', lw=0,color='blue',markerfacecolor='blue', markersize=10),
    Line2D([0], [0], lw=2,color=hmcmp[1], linestyle='-', marker='o',
                    markersize=15, markerfacecoloralt=hmcmp[-1],fillstyle="bottom")
    ]
    legendNames = [
               "HStart","HHeat"
              ]
    ax.legend(legendShapes, legendNames,loc="lower left",fancybox=True, shadow=True) 