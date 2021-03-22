# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 15:04:45 2021

@author: Arjun
"""
import mne
import numpy as np

# function to create eeg visualization and save it to corresponding filepath
def eeg_viz(data, xstart, xend, filepath):        
    # sensor names
    ch_names = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2', 'F7', 'F8', 'T7', 'T8',
            'P7', 'P8', 'Fz', 'Cz', 'Pz', 'Oz', 'FC1', 'FC2', 'CP1', 'CP2', 'FC5', 'FC6',
            'CP5', 'CP6', 'FT9', 'FT10', 'FCz', 'AFz', 'F1', 'F2', 'C1', 'C2', 'P1', 'P2',
            'AF3', 'AF4', 'FC3', 'FC4', 'CP3', 'CP4', 'PO3', 'PO4', 'F5', 'F6', 'C5', 'C6',
            'P5', 'P6', 'AF7', 'AF8', 'FT7', 'FT8', 'TP7', 'TP8', 'PO7', 'PO8', 'Fpz', 'CPz', 'POz', 'TP10']

    ch_types = ['eeg' for j in range(64)] # eeg type for the 64 different sensors
    
   
    info = mne.create_info(ch_names=ch_names, sfreq=500, ch_types=ch_types)
    
    info.set_montage("standard_1020") # for sensor location
    
    evoked = mne.EvokedArray(np.zeros(((xend - xstart), 64)).transpose(), info) # create structure to get visualization
    
    def eeg_heatmap(evoked, band, data): # helper function to create heatmap and save it to filepath
        if band == 'theta': # theta band 
            data = data.iloc[xstart:xend, 10:74]
        elif band == 'alpha': # alpha band
            data = data.iloc[xstart:xend, 74:138]
        elif band == 'beta': # beta band
            data = data.iloc[xstart:xend, 138:]
        
        evoked.data = np.array(data).transpose() # create sturcture to get heatmap with given data
        # create heatmap 
        fig = evoked.plot_topomap(times=[0], ch_type='eeg', time_format='', extrapolate='head',
                                              cmap='jet', colorbar=False, size=5, sensors='kX', show=False)
        
        fig.savefig(filepath + band)
    
    eeg_heatmap(evoked, 'theta', data)
    eeg_heatmap(evoked, 'alpha', data)
    eeg_heatmap(evoked, 'beta', data)