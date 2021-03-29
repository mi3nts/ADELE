# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 10:32:33 2021

@author: Razor Drive
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cv2
from matplotlib.backends.backend_pdf import PdfPages
import fitz
from sklearn.cluster import KMeans
import scipy.signal as sci
from dataclasses import dataclass
import math
#BUCKETSIZE determines how wide the groups that the event creation algorithm uses. Larger buckets would mean that a wider area of peaks is added up to find the most significant events.
BUCKETSIZE = 500
@dataclass(order = True)
class Peak:
    index: int
    prom: float
    
@dataclass(order=True)
class Group:
    totalProm: float
    start: int
    end: int
    count: int

@dataclass(order=True)
class TimeRange:
    start
    end
    number
    
def CreateFigure(nordata, altdata,value,title,unit):
    plt.clf()
    plt.xticks(ticks = range(0,altdata.shape[0],int(altdata.shape[0]/3)))
    plt.ylabel(unit)
    plt.title(title)
    plt.axhline(nordata[value].mean(), color = 'xkcd:blue with a hint of purple')
    plt.plot_date(nordata.loc[:,'Datetime'],altdata.loc[:,value],xdate = True,color = 'xkcd:light eggplant', linestyle = '-', marker = "None",linewidth = 1)
    return plt.gcf()

def CreateClusterFigure(nordata,altdata,value,title,unit):
    plt.clf()
    plt.xticks(ticks = range(0,nordata.shape[0],int(nordata.shape[0]/3)))
    plt.ylabel(unit)
    plt.title(title)
    plt.axhline(nordata[value].mean(), color = 'xkcd:blue with a hint of purple')
    plt.scatter(nordata.loc[::100,'Datetime'],altdata.loc[::100,value],c=altdata.loc[::100,'Colors'], marker = "o",lw=0,s=2)
    return plt.gcf()
    
#This function finds peaks across the given column, and places their indicies and prominences into the returned list
def FindPeaks(coli):
    peaks,properties = sci.find_peaks(coli, distance = 250, prominence = (.5,1))
    peakList =[]
    for i in range(len(peaks)):
        nuPeak = Peak(peaks[i],properties['prominences'][i])
        peakList.append(nuPeak)
    return peakList
"""
#This funciton adds up all the peak prominences found into a set of buckets that span the data set.
def FillBuckets(peakList,dataSize):
    buckets = np.zeros_like(peakList,dtype = float, shape = math.ceil(dataSize/BUCKETSIZE))
    for peak in peakList:
        buckets[math.ceil(peak.index/BUCKETSIZE)-1] += peak.prom
    return buckets
"""
#This creates groups which indicate sets of peaks with at most BUCKETSIZE space between consecutive members of the group
#The group structure then contains the start index, end index, total prominence, and number of peaks in the group
def GroupPeaks(peakList):
    peakGroups = []
    currentGroup = Group(peakList[0].prom, peakList[0].index, peakList[0].index,1)
    for i in range(1,len(peakList)):
        if peakList[i].index >= (currentGroup.end+BUCKETSIZE):
            peakGroups.append(currentGroup)
            currentGroup = Group(peakList[i].prom, peakList[i].index,peakList[i].index,1)
        else:
            currentGroup.totalProm = currentGroup.totalProm + peakList[i].prom
            currentGroup.end = peakList[i].index
            currentGroup.count = currentGroup.count + 1
    peakGroups.append(currentGroup)
    return peakGroups

#This function selects the most prominent groups and returns them.
# It can be configured to operate off of a fixed number, peakCount, or 
# with a threshold
def CleanGroups(groupList,peakCount):
    groupList.sort(reverse = True)
    print(groupList)
    print("peakCount2" + str(peakCount))
    print(len(groupList))
    cleanedGroups= []
    """
    x = 0
    while(x < len(groupList) and groupList[x].totalProm > 3):
        cleanedGroups.append(groupList[x].start)
        x = x+1
    """
    if(len(groupList) < peakCount):
        print("Fewer groups than expected")
        peakCount = len(groupList)
    for i in range(peakCount):
        cleanedGroups.append(groupList[i].start)
    cleanedGroups.sort()
    return cleanedGroups
"""
def CleanPeaks(peakList,peakCount,dataSize):
    buckets = FillBuckets(peakList,dataSize)
    indicies = np.flip(np.argsort(buckets))[:peakCount]
    print(buckets[indicies[0]])
    print(buckets[indicies[1]])
    print(buckets[indicies[2]])
    print(indicies)
    results = []
    for index in indicies:
        results.append(index)
    peakList.sort()
    results.sort()
    checkIndex = 0;
    cleanPeaks = []
    for item in results:
        curMaxVal = -1;
        curMaxIndex = -1;
        while (peakList[checkIndex].index < (item*BUCKETSIZE)):
            checkIndex = checkIndex +1
        while(peakList[checkIndex].index < ((item*BUCKETSIZE) +BUCKETSIZE-1))and (checkIndex < len(peakList)):
            if(peakList[checkIndex].prom > curMaxVal):
                curMaxIndex = peakList[checkIndex].index
                curMaxVal = peakList[checkIndex].prom
            checkIndex = checkIndex + 1
        cleanPeaks.append(curMaxIndex)
    return cleanPeaks
"""
#This funciton identifies events by calling the other functions and then assigns labels
def CreateEvents(nordata,norldata):
    peakList = []
    peakCount= math.ceil(nordata.shape[0]/15000)
    print("PeakCount" +str(peakCount))
    for column in range(1,norldata.shape[1]):
        peakList.extend(FindPeaks(np.asarray(norldata.iloc[:,column])))
    peakList.sort()
    """
    clean = CleanPeaks(peakList,peakCount,nordata.shape[0])
    """
    groups = GroupPeaks(peakList)
    clean = CleanGroups(groups,peakCount)
    labels= []
    labels = np.zeros_like(labels,dtype = int, shape = nordata.shape[0])
    eventNum = 0;
    for i in range(labels.size):
        if eventNum < len(clean) and i == clean[eventNum]:
            eventNum = eventNum + 1
        labels[i] = eventNum
    return labels

#This function returns a list of time range objects
#For each event, there is a TimeRange object that has a start time, end time, and event number
def CreateTimeRanges(labellist,datetimes):
    timeRanges = []
    currentRange = TimeRange(start = datetimes[0],end = datetimes[0], number = 0)
    for i in range(1,len(labellist)):
        if(labellist[i] != currentRange.number):
            currentRange.end = datetimes[i-1]
            timeRanges.append(currentRange)
            currentRange = TimeRange(start = datetimes[i],end=datetimes[i],number = labellist[i])
    currentRange.end = datetimes[len(labellist-1)]
    timeRanges.append(currentRange)
    return timeRanges

plt.rcdefaults()
plt.ioff()
data = pd.DataFrame(pd.read_csv('C:\Data\School\SeniorDesign\data.csv', header = 0,usecols=[0,1,2,3,4,5,6,7,8,9,10]))
ekgColNums = [0]
ekgColNums.extend(range(10,202))
badrows = range(100000,141536) #The last portions of the data seem to heavily skew the results, and so are thrown out here. 
ekg = pd.DataFrame(pd.read_csv('C:\Data\School\SeniorDesign\data.csv', header = 0,usecols = ekgColNums))
print(ekg.shape[1])
ekg = ekg.drop(badrows)
data = data.drop(badrows)
ekg = ekg.dropna(axis = 0)
data = data.dropna(axis = 0)
print(ekg.shape[0])
print(data.shape[0])
alterdata = pd.DataFrame(columns = data.columns)
alterdata['Datetime']=range(data.shape[0])
#alterdata is the data with the running average applied, and is what is displayed
normadata=ekg

normadata=normadata.drop(columns=['Datetime'])


normadata['Datetime']=range(data.shape[0])
#Normadata contains all the data with the time stamp reduced to an incrementing int, 
#and all values rescaled to range from 0 to 1 wihtin their respecitve graphs
print ("size "+ str(normadata.shape[0]))
normadata=(normadata-normadata.min())/(normadata.max()-normadata.min())
normadata['Datetime']=normadata['Datetime']
print ("Asize "+ str(normadata.shape[0]))
labels = CreateEvents(data,normadata)
pages = PdfPages("Graphs9.pdf")
"""
k = 10
model = KMeans(n_clusters=k)
"""
alterdata['Temp']=data['Temp'].rolling(20000,center = True,min_periods = 1).mean()
alterdata['HR']=data['HR'].rolling(8000,center=True, min_periods = 1).mean()
alterdata['HRV_rMSSD']=data['HRV_rMSSD'].rolling(8000,center=True, min_periods = 1).mean()
alterdata['GSR_uS']=data['GSR_uS'].rolling(6000,center = True,min_periods = 1).mean()
alterdata['SpO2']=data['SpO2'].rolling(6000,center=True, min_periods = 1).mean()
alterdata['CT_buller']=data['CT_buller'].rolling(8000,center=True, min_periods = 1).mean()
alterdata['PupilCenter_Distance']=data['PupilCenter_Distance'].rolling(18500,center = True,min_periods = 1).mean()
alterdata['PupilDiameterDifference']=data['PupilDiameterDifference'].rolling(18500,center=True, min_periods = 1).mean()
alterdata['AveragePupilDiameter']=data['AveragePupilDiameter'].rolling(18500,center=True, min_periods = 1).mean()
"""
labels= model.fit_predict(normadata)
"""
alterdata['Labels']=labels
alterdata['Fp1_theta']=normadata['Fp1_theta']
colors = ['xkcd:purple','xkcd:light green', 'xkcd:turquoise','xkcd:orange','xkcd:beige','xkcd:hot pink','xkcd:light brown','xkcd:navy blue','xkcd:lilac','xkcd:black','xkcd:green']
alterdata['Colors']=alterdata.Labels.map({0:colors[0],1:colors[1],2:colors[2],3:colors[3],4:colors[4],5:colors[5],6:colors[6],7:colors[7],8:colors[8],9:colors[9],10:colors[10]})
normadata['Colors']=alterdata.Labels.map({0:colors[0],1:colors[1],2:colors[2],3:colors[3],4:colors[4],5:colors[5],6:colors[6],7:colors[7],8:colors[8],9:colors[9],10:colors[10]})
print(labels)

pages.savefig(CreateClusterFigure(data,alterdata,'Temp','Temperature','Celcius'))

pages.savefig(CreateClusterFigure(data,alterdata,'HR','Heart Rate','BPM'))
pages.savefig(CreateClusterFigure(data,alterdata,'HRV_rMSSD','Heart Rate Variability','milliseconds'))
pages.savefig(CreateClusterFigure(data,alterdata,'GSR_uS','Galvanic Skin Response','uS'))
pages.savefig(CreateClusterFigure(data,alterdata,'SpO2','Blood Oxygen','Percentage'))
pages.savefig(CreateClusterFigure(data,alterdata,'CT_buller','Estimated Core Temperature','Celcius'))
pages.savefig(CreateClusterFigure(data,alterdata,'PupilCenter_Distance','Interpupilary Distance','mm'))
pages.savefig(CreateClusterFigure(data,alterdata,'PupilDiameterDifference','Pupil Diameter Difference','mm'))
pages.savefig(CreateClusterFigure(data,alterdata,'AveragePupilDiameter','Average Pupil Diameter','mm'))
pages.savefig(CreateClusterFigure(data,alterdata,'Fp1_theta','x','y'))
pages.close()
print("done")
