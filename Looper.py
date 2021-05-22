import fitz
import pandas as pd
import numpy as np
import docGenerator
import tableOfContentsGenerator as TOCGenerator
import bioPlotter
import kmeansClusters
import coverPage
import areaGetter
import os
import argparse

# configure command line entry of trial details
parser = argparse.ArgumentParser()

parser.add_argument('--trial', nargs='+',
                    help="Provide trial details in the following manner: 'Title (in quotation marks)' YYYY MM DD TXX UXXX AA. Replace X for User and Trial as necessary. Replace AA for version of Tobii Pro used.")
args = parser.parse_args()

trial_details_full = args._get_kwargs()[0][1]

event_descriptor = trial_details_full[0]

if len(trial_details_full) == 7:
    tobii_ver = trial_details_full[-1]
    trial_details = trial_details_full[1:-1]
else:
    tobii_ver = None
    trial_details = trial_details_full[1:]

# paths for objects within BM3
csv_path = "../../../objects/" + "/".join(trial_details) + "/ADELE/" + "_".join(trial_details) + "_ADELE.csv"
fullstream_path = "../../../raw/" + "/".join(trial_details) + "/Tobii" + tobii_ver + "/" + "_".join(trial_details) + "_Tobii" + tobii_ver + "/segments/1/fullstream.mp4"
report_path = "../../../visuals/" + "/".join(trial_details) + "/ADELE/" + "_".join(trial_details)
report_content_path = report_path + "/static/"

# create directory for report and statics of report
os.makedirs(report_content_path, exist_ok=True)

full_data = pd.read_csv(csv_path)

finalReportDoc = fitz.open()

# clustering algorithm used
num_of_clusters = 5
clusters = kmeansClusters.createClusters(full_data,num_of_clusters)

# cover page
coverPage = coverPage.createCoverPage("Event: " + event_descriptor,"Clustering: KMeans, n_clusters = %d" % num_of_clusters,"_".join(trial_details))

# start and end indexes for each cluster
dataStartArray = [i[1][0] for i in clusters.items()]
dataEndArray = [i[1][1] for i in clusters.items()]

# cluster labels 
titleArray = ["Cluster " + str(i) + ": from " + str(dataStartArray[i]/500) + " to " + str(dataEndArray[i]/500) + " seconds" for i,j in enumerate(dataStartArray)]

# array of text files to get the active areas
textArray = [report_content_path + "active_areas_%d.txt" % i for i in range(num_of_clusters)]

# create text files with active areas
i=0
for doc in textArray:
    file = open(doc, "w")
    areas = areaGetter.GetActiveAreas(dataStartArray[i],dataEndArray[i],"alpha",full_data)
    zipped_areas = list(zip(*areas))
    for j in range(len(zipped_areas)):
        file.write(zipped_areas[j][0] + ": " + zipped_areas[j][1] + " - " + zipped_areas[j][2] + " - " + zipped_areas[j][3] + "\n")
    file.close()
    i=i+1


tableOfContents = TOCGenerator.generateTOC(finalReportDoc, "aLooperExample.pdf", report_content_path)

bio1 = "HR"
bio2 = "Temp"
bio3 = "AveragePupilDiameter"
bio4 = "HRV_rMSSD"
vid_filename = fullstream_path

startPoint = fitz.Point(100, 150)

# creating the body of the report
for index, entry in enumerate(dataStartArray):
    

    currentDataEnd = dataEndArray[index]
    currentTitle = titleArray[index]
    currentText = textArray[index]
    doc_filename = "SampleReport_page%i.pdf"%(index)

    generatedDoc = docGenerator.generateDoc(currentTitle, full_data, entry, currentDataEnd,
                                            bio1, bio2, bio3, bio4, vid_filename, currentText, doc_filename, index,report_content_path)
    startPoint = TOCGenerator.append_TOC(finalReportDoc, generatedDoc, currentTitle, "SampleReport.pdf", startPoint, report_content_path)
    percentage = round(((index+1) / len(dataStartArray)) * 100)
    print("Document %i percent complete..."%(percentage))

# combining title page and body
# if you want to generate a test pdf, change "_REPORT" to whatever
TOCGenerator.append_CoverPage(finalReportDoc, coverPage, "_".join(trial_details) + "_REPORT.pdf",report_content_path)