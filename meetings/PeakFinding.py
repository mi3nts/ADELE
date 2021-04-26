# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 13:33:30 2021

@author:
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
from datetime import datetime
import math
import re

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
    start: datetime
    end: datetime
    number: int

@dataclass(order=True)
class simGroup:
    start: int
    end: int
#This function finds peaks across the given column, and places their indicies and prominences into the returned list
def FindPeaks(coli):
    peaks,properties = sci.find_peaks(coli, distance = 250, prominence = (.30,1))
    peakList =[]
    for i in range(len(peaks)):
        nuPeak = Peak(peaks[i],properties['prominences'][i])
        peakList.append(nuPeak)
    return peakList

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

#This funciton identifies events by calling the other functions and then assigns labels
def CreateEvents(nordata):
    peakList = []
    norldata = nordata
    norldata= norldata.iloc[:,10:]
    print (norldata.shape[0])
    print (norldata.shape[1])
    norldata=(norldata-norldata.min())/(norldata.max()-norldata.min())
    peakCount= math.ceil(norldata.shape[0]/15000)
    for column in range(0,norldata.shape[1]):
        peakList.extend(FindPeaks(np.asarray(norldata.iloc[:,column])))
    peakList.sort()
    """
    clean = CleanPeaks(peakList,peakCount,nordata.shape[0])
    """
    groups = GroupPeaks(peakList)
    clean = CleanGroups(groups,peakCount)
    finalGroups = []
    temp = simGroup(start = 0, end = 0)
    for i in clean:
        temp.end = i-1
        finalGroups.append(temp)
        temp = simGroup(start = i, end = i)
    temp.end = norldata.shape[0]
    finalGroups.append(temp)
    return finalGroups
"""
    labels= []
    labels = np.zeros_like(labels,dtype = int, shape = norldata.shape[0])
    eventNum = 0;
    for i in range(labels.size):
        if eventNum < len(clean) and i == clean[eventNum]:
            eventNum = eventNum + 1
        labels[i] = eventNum
    return labels
"""
#This function returns a list of time range objects
#For each event, there is a TimeRange object that has a start time, end time, and event number
def CreateTimeRanges(labellist,datetimes):
    timeRanges = []
    print(datetimes)
    currentRange = TimeRange(start = datetimes.iloc[0],end = datetimes.iloc[0], number = 0)
    for i in range(1,len(labellist)):
        if(labellist[i] != currentRange.number):
            currentRange.end = datetimes.iloc[i-1]
            timeRanges.append(currentRange)
            currentRange = TimeRange(start = datetimes.iloc[i],end=datetimes.iloc[i],number = labellist[i])
    currentRange.end = datetimes[len(labellist-1)]
    timeRanges.append(currentRange)
    return timeRanges

