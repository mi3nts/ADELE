# ADELE: Automated Documentation to Extract Learning from EEG 
# Authors

* Cristian Garces 
* Rami Jaber
* Bradley Krakar 
* Jesse Ladyman 
* Ash Fernando
* Arjun Sridhar
* Shawhin Talebi

# Introduction
The purpose of this project is to take in biometrics and EEG ratings, automatically split them apart into distinct events, correlate these events to what stimuli were occurring at the time using unsupervised classification, and display these results in a clear, easy to parse fashion.

ADELE is more advanced than other solutions in that it handles the data analysis almost entirely automatically. It searches the data for correlations between different EEG bands and biometrics and splits them off together with their timestamps and stimuli, instead of manually requiring humans to track the different events and correlate them with the readings.

# Installation
1. [Download the repository](https://github.com/mi3nts/ADELE/archive/refs/heads/main.zip), or use HTTPS: `git clone https://github.com/mi3nts/ADELE.git`.
2. From the root of the repository, run `pip install -r requirements.txt` to install all required Python dependencies.

# Usage and Documentation

An example command line execution on ADELE is shown below:

~~~bash
$ python Looper.py --trial "Twitter scrolling" 2020 06 05 T05 U00T 01
~~~

To run Looper, execute the "--trial" argument and provide the following (relevant example argument in parentheses):
* an event descriptor ("Twitter scrolling") - this would show on the title page
* Year, month, date of tiral (2020 06 05)
* Trial and user data (T05 U00T)
* Tobii Pro version used (01)

Then, the event detection algorithm used will separate the total time window into subgroups, with each page of the report dedicated to one of these subgroups. There will be a progress update on the command line with the creation of each page. 

The final report can be accessed at BM3/visuals/YYYY/MM/DD/TXX/UXX/ADELE/YYYY/MM/DD/TXX/UXX

Libraries required:
* [Pandas](https://pandas.pydata.org/)
* [Numpy](https://numpy.org/)
* [OpenCV](https://github.com/opencv/opencv)
* [PyMuPDF](https://github.com/pymupdf/PyMuPDF)
* [MNE](https://mne.tools/stable/index.html)

# Contact

* Cristian Garces: cxg150730@utdallas.edu 
* Rami Jaber: rxj180009@utdallas.edu 
* Bradley Krakar: bjk170630@utdallas.edu 
* Jesse Ladyman: jessedavidladyman@gmail.com

## License
If you find value in this dashboard please use the following citation: 

`Garces, C., Jaber, R., Krakar, B., Ladyman J., Sridhar, A., Fernando, B., Talebi, S. ADELE: Automated Documentation to Extract Learning from EEG. 2021. https://github.com/mi3nts/ADELE`

__Bibtex__:
```
@misc{ADELE,
authors={Cristian Garces, Rami Jaber, Bradley Krakar, Jesse Ladyman, Arjun Sridhar, Bharana Fernando, & Shawhin Talebi},
title={ADELE: Automated Documentation to Extract Learning from EEG},
howpublished={https://github.com/mi3nts/ADELE}
year={2021}
}
```
