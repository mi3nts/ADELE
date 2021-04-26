import fitz
import pandas as pd
import numpy as np
import docGenerator
import tableOfContentsGenerator as TOCGenerator
import bioPlotter
import kmeansClusters
import coverPage

data=pd.read_csv('2020_06_04_T05_U00T_ADELE.csv')
newDoc = fitz.open()

# clustering algorithm used
clusters = kmeansClusters.createClusters(data,7)

# cover page
titlePage = coverPage.createCoverPage("Event: Scrolling Twitter","Clustering: KMeans, n_clusters = 5")

# start and end indexes for each cluster
dataStartArray = [i[1][0] for i in clusters.items()]
dataEndArray = [i[1][1] for i in clusters.items()]

# cluster labels 
titleArray = ["Cluster " + str(i) + ": from " + str(dataStartArray[i]/500) + " to " + str(dataEndArray[i]/500) + " seconds" for i,j in enumerate(dataStartArray)]

tableOfContents = TOCGenerator.generateTOC(newDoc, "aLooperExample.pdf")

bio1 = "HR"
bio2 = "Temp"
bio3 = "AveragePupilDiameter"
bio4 = "HRV_rMSSD"
vid_filename = "fullstream.mp4"
textPlaceholder = "soon.jpg"
startPoint = fitz.Point(100, 150)

# creating the body of the report
for index, entry in enumerate(dataStartArray):
    currentDataEnd = dataEndArray[index]
    currentTitle = titleArray[index]
    doc_filename = "aLooperTestDoc_page%i.pdf"%(index)

    generatedDoc = docGenerator.generateDoc(currentTitle, data, entry, currentDataEnd,
                                            bio1, bio2, bio3, bio4, vid_filename, textPlaceholder, doc_filename)
    startPoint = TOCGenerator.append_TOC(newDoc, generatedDoc, currentTitle, "aLooperTestTOC.pdf", startPoint)
    percentage = round(((index+1) / len(dataStartArray)) * 100)
    print("Document %i percent complete..."%(percentage))

# combining title page and body
titlePage.insert_pdf(newDoc)
titlePage.save("final_report.pdf")