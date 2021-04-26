# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 13:55:39 2021

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
class p(object):
        def __init__(self,name):
            self.name = name
        def __repr__(self):
            return self.name
        def __str__(self):
            return self.name
        
brainmap = {
    'Fpz':'Prefrontal Cortex',
    'Fp1':'Prefrontal Cortex',
    'Fp2':'Prefrontal Cortex',
    'AF7':'Prefrontal Cortex',
    'AF3':'Prefrontal Cortex',
    'AFz':'Prefrontal Cortex',
    'AF4':'Prefrontal Cortex',
    'AF8':'Prefrontal Cortex',
    'F7' :'Premotor Cortex',
    'F5':'Premotor Cortex',
    'F3':'Premotor Cortex',
    'F1':'Premotor Cortex',
    'Fz':'Premotor Cortex',
    'F2':'Premotor Cortex',
    'F4':'Premotor Cortex',
    'F6':'Premotor Cortex',
    'F8':'Premotor Cortex',
    'FT9':'Auditory Association Area',
    'FT7':'Brocas Area',
    'FC5':'Primary Motor Cortex',
    'FC3':'Primary Motor Cortex',
    'FC1':'Primary Motor Cortex',
    'FCz':'Primary Motor Cortex',
    'FC2':'Primary Motor Cortex',
    'FC4':'Primary Motor Cortex',
    'FC6':'Primary Motor Cortex',
    'FT8': 'Brocas Area',
    'FT10':'Auditory Association Area',
    'T7':'Auditory Cortex',
    'C5':'Priamry Sensory Cortex',
    'C3':'Priamry Sensory Cortex',
    'C1':'Priamry Sensory Cortex',
    'Cz':'Priamry Sensory Cortex',
    'C2':'Priamry Sensory Cortex',
    'C4':'Priamry Sensory Cortex',
    'C6':'Priamry Sensory Cortex',
    'T8':'Auditory Cortex',
    'TP7':'Wernickes Area',
    'CP5':'Somatic Sensory Association Area',
    'CP3':'Somatic Sensory Association Area',
    'CP1':'Somatic Sensory Association Area',
    'CPz':'Somatic Sensory Association Area',
    'CP2':'Somatic Sensory Association Area',
    'CP4':'Somatic Sensory Association Area',
    'CP6':'Somatic Sensory Association Area',
    'TP8':'Wernickes Area',
    'TP10':'Wernickes Area',
    'P7':'Somatic Sensory Association Area',
    'P5':'Somatic Sensory Association Area',
    'P3':'Somatic Sensory Association Area',
    'P1':'Somatic Sensory Association Area',
    'Pz':'Somatic Sensory Association Area',
    'P2':'Somatic Sensory Association Area',
    'P4':'Somatic Sensory Association Area',
    'P6':'Somatic Sensory Association Area',
    'P8':'Somatic Sensory Association Area',
    'PO7':'Visual Association Area',
    'PO3':'Visual Association Area',
    'POz':'Visual Association Area',
    'PO4':'Visual Association Area',
    'PO8':'Visual Association Area',
    'O1':'Visual Cortex',
    'Oz':'Visual Cortex',
    'O2':'Visual Cortex',
    'REF':'NAN',
    'GND':'NAN'
    }
broadmannmapping ={
    'Fpz':'ba10L',
    'Fp1':'ba10L',
    'Fp2':'ba10R',
    'AF7':'ba46L',
    'AF3':'ba09L',
    'AFz':'ba09L',
    'AF4':'ba09R',
    'AF8':'ba46R',
    'F7' :'ba47L',
    'F5':'ba46L',
    'F3':'ba08L',
    'F1':'ba08L',
    'Fz':'baO8L',
    'F2':'ba08R',
    'F4':'ba08R',
    'F6':'ba46R',
    'F8':'ba45R',
    'FT9':'ba20L',
    'FT7':'ba47L',
    'FC5':'BROCLA',
    'FC3':'ba06L',
    'FC1':'ba06L',
    'FCz':'ba06R',
    'FC2':'ba06R',
    'FC4':'ba06R',
    'FC6':'ba44R',
    'FT8': 'ba47R',
    'FT10':'ba20R',
    'T7':'ba42L',
    'C5':'ba42L',
    'C3':'ba02L',
    'C1':'ba05L',
    'Cz':'ba05L',
    'C2':'ba05R',
    'C4':'ba01R',
    'C6':'ba41R',
    'T8':'ba21R',
    'TP7':'ba21L',
    'CP5':'ba40L',
    'CP3':'ba02L',
    'CP1':'ba05L',
    'CPz':'ba05R',
    'CP2':'ba05R',
    'CP4':'ba40R',
    'CP6':'ba40R',
    'TP8':'ba21R',
    'TP10':'ba21R',
    'P7':'ba37L',
    'P5':'ba39L',
    'P3':'ba39L',
    'P1':'ba07L',
    'Pz':'ba07R',
    'P2':'ba07R',
    'P4':'ba39R',
    'P6':'ba39R',
    'P8':'ba37R',
    'PO7':'ba19L',
    'PO3':'ba19L',
    'POz':'ba17L',
    'PO4':'ba19R',
    'PO8':'ba19R',
    'O1':'ba19L',
    'Oz':'ba17R',
    'O2':'ba18R',
    'REF':'NAN',
    'GND':'NAN'
    }
broadmanntoarea ={
    'ba01':'Primary Sensory Cortex',
    'ba02':'Primary Sensory Cortex',
    'ba03':'Primary Sensory Cortex',
    'ba04':'Primary Motor Cortex',
    'ba05':'Somatic Sensory Association Area',
    'ba06':'Premotor Cortex',
    'ba07':'Somatic Sensory Association Area',
    'ba08':'Prefrontal Cortex',
    'ba09':'Prefrontal Cortex',
    'ba10':'Prefrontal Cortex',
    'ba11':'Prefrontal Cortex',
    'ba12':'Prefrontal Cortex',
    'ba17':'Visual Cortex',
    'ba18':'Visual Cortex',
    'ba19':'Visual Association Area',
    'ba20':'Temporal',
    'ba21':'Temporal',
    'ba22':'Wernickes Area',
    'ba37':'Temporal',
    'ba38':'Temporal',
    'ba39':'Wernickes Area',
    'ba40':'Wernickes Area',
    'ba41':'Auditory Cortex',
    'ba42':'Auditory Cortex',
    'ba43':'Frontal Cortex',
    'ba44':'Frontal Cortex',
    'BROCLA':'Brocas Area',
    'ba45':'Frontal Cortex',
    'ba46':'Frontal Cortex',
    'ba47':'Frontal Cortex',
    }
areamap = {
    'Prefrontal Cortex':'Involved in decision making and abstract thought',
    'Premotor Cortex':'Involved in planning of movement',
    'Brocas Area':'Responsible for speech production',
    'Auditory Cortex':'Processes sound',
    'Auditory Association Area':'Responsible for high level processing of sound, such as memory',
    'Primary Motor Cortex':'Executes Movement',
    'Primary Sensory Cortex':'Main receptive area for the senses, especially touch',
    'Wernickes Area':'Involved in understanding speech',
    'Somatic Sensory Association Area':'Involved in high level touch interpretation',
    'Visual Association Area':'Involved in high level processing of visual stimuli',
    'Visual Cortex':'Processes visual stimuli'
    }
#Defines active areas as those where their values normalized compared to all sensors on that band
#are greater than or equal to .8. Currently only actually examines first row
#in each time range, as per the heatmaps functionality
def GetActiveAreas(times,band,data):
    first = data.index[data['Datetime']==times.start].values[0]
    last =  data.index[data['Datetime']==times.end].values[0]
    if band == 'theta':
        data = data.iloc[first:last, 0:64]
    elif band == 'alpha':
        data = data.iloc[first:last, 64:128]
    elif band =='beta':
        data = data.iloc[first:last, 128:]
    min = data.min()
    max = data.max()
    normalized = (data- min)/(max-min)
    columns = []
    for i in range(normalized.shape[1]):
        if normalized.iloc[0,i]>= .8:
            
            columns.append(normalized.columns[i])
    areas = FindAreas(columns)
    return areas

def FindAreas(columns):
    areamark = [False,False,False,False,False,False,False,False,False,False,False]
    areas = []
    for sensor in columns:
        if brainmap[sensor.split('_')[0]] == 'Prefrontal Cortex':
            if areamark[0]== False:
                areas.append('Prefrontal Cortex')
                areas.append(areamap['Prefrontal Cortex'])
                areamark[0]= True
        elif brainmap[sensor.split('_')[0]] == 'Premotor Cortex':
            if areamark[1]== False:
                areas.append('Premotor Cortex')
                areas.append(areamap['Premotor Cortex'])
                areamark[1]= True
        elif brainmap[sensor.split('_')[0]] == 'Auditory Association Area':
            if areamark[2]== False:
                areas.append('Auditory Association Area')
                areas.append(areamap['Auditory Association Area'])
                areamark[2]= True
        elif brainmap[sensor.split('_')[0]] == 'Brocas Area':
            if areamark[3]== False:
                areas.append('Brocas Area')
                areas.append(areamap['Brocas Area'])
                areamark[3]= True
        elif brainmap[sensor.split('_')[0]] == 'Primary Motor Cortex':
            if areamark[4]== False:
                areas.append('Primary Motor Cortex')
                areas.append(areamap['Primary Motor Cortex'])
                areamark[4]= True        
        elif brainmap[sensor.split('_')[0]] == 'Auditory Cortex':
            if areamark[5]== False:
                areas.append('Auditory Cortex')
                areas.append(areamap['Auditory Cortex'])
                areamark[5]= True          
        elif brainmap[sensor.split('_')[0]] == 'Priamry Sensory Cortex':
            if areamark[6]== False:
                areas.append('Priamry Sensory Cortex')
                areas.append(areamap['Primary Sensory Cortex'])
                areamark[6]= True 
        elif brainmap[sensor.split('_')[0]] == 'Wernickes Area':
            if areamark[7]== False:
                areas.append('Wernickes Area')
                areas.append(areamap['Wernickes Area'])
                areamark[7]= True  
        elif brainmap[sensor.split('_')[0]] == 'Somatic Sensory Association Area':
            if areamark[8]== False:
                areas.append('Somatic Sensory Association Area')
                areas.append(areamap['Somatic Sensory Association Area'])
                areamark[8]= True  
        elif brainmap[sensor.split('_')[0]] == 'Visual Association Area':
            if areamark[9]== False:
                areas.append('Visual Association Area')
                areas.append(areamap['Visual Association Area'])
                areamark[9]= True  
        elif brainmap[sensor.split('_')[0]] == 'Visual Cortex':
            if areamark[10]== False:
                areas.append('Visual Cortex')
                areas.append(areamap['Visual Cortex'])
                areamark[10]= True  
        
    return areas

#This function calls GetActiveAreas for all bands and time ranges, and puts the output in a text file.
def CreateText(times,data):
    File = open("EEGMARKS.txt","w")
    for rang in times:
        File.write("Timeframe: " + str(rang.start) + " to "+ str(rang.end) + "\n")
        File.write("Theta: "+ str(GetActiveAreas(rang,'theta',data))+ "\n")
        File.write("Alpha: "+ str(GetActiveAreas(rang,'alpha',data))+ "\n")                    
        File.write("Beta: "+ str(GetActiveAreas(rang,'beta',data))+"\n" + "\n")
    File.close()               