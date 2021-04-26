# ADELE: Automated Documentation to Extract Learning from EEG 
# Authors
* Ash Fernando
* Cristian Garces 
* Rami Jaber
* Bradley Krakar 
* Jesse Ladyman 
* Shawhin Talebi

# Introduction
The purpose of this project is to take in biometrics and EEG ratings, automatically split them apart into distinct events, correlate these events to what stimuli were occurring at the time using unsupervised classification, and display these results in a clear, easy to parse fashion.

ADELE is more advanced than other solutions in that it handles the data analysis almost entirely automatically. It searches the data for correlations between different EEG bands and biometrics and splits them off together with their timestamps and stimuli, instead of manually requiring humans to track the different events and correlate them with the readings.

# Installation
1. [Download the repository](https://github.com/mi3nts/ADELE/archive/refs/heads/main.zip), or use HTTPS: `git clone https://github.com/mi3nts/ADELE.git`.
2. From the root of the repository, run `pip install -r requirements.txt` to install all required Python dependencies
*Keep in mind that this program is developed using Python 3.7*

# Usage and Documentation
Edit the Looper.py file and replace the data location with the file that you want to read, then set the number of clusters you want (and adjust any factors such as title page text and file name) and run the program

Libraries required:
* [Pandas](https://pandas.pydata.org/)
* [Numpy](https://numpy.org/)
* [OpenCV](https://github.com/opencv/opencv)
* [PyMuPDF](https://github.com/pymupdf/PyMuPDF)
* [MNE](https://mne.tools/stable/index.html)

# Contact

Cristian Garces: cxg150730@utdallas.edu 
Rami Jaber: rxj180009@utdallas.edu 
Bradley Krakar: bjk170630@utdallas.edu 
Jesse Ladyman: jessedavidladyman@gmail.com
