import fitz
import pandas as pd
import numpy as np
import docGenerator
import tableOfContentsGenerator as TOCGenerator
import bioPlotter

data=pd.read_csv('2020_06_04_T05_U00T_ADELE.csv')
newDoc = fitz.open()

dataStartArray = [10000, 30000, 60000, 80000, 105000]
dataEndArray = [20000, 50000, 75000, 100000, 110000]
titleArray = ["1: 10000-20000", "2: 30000-50000", "3: 60000-75000", "4: 80000-100000", "5: 105000-110000"]
tableOfContents = TOCGenerator.generateTOC(newDoc, "aLooperExample.pdf")

bio1 = "HR"
bio2 = "Temp"
bio3 = "AveragePupilDiameter"
bio4 = "HRV_rMSSD"
vid_filename = "fullstream.mp4"
textPlaceholder = "textPlaceholder.png"
startPoint = fitz.Point(100, 150)


for index, entry in enumerate(dataStartArray):
    currentDataEnd = dataEndArray[index]
    currentTitle = titleArray[index]
    doc_filename = "aLooperTestDoc_page%i.pdf"%(index)

    generatedDoc = docGenerator.generateDoc(currentTitle, data, entry, currentDataEnd,
                                            bio1, bio2, bio3, bio4, vid_filename, textPlaceholder, doc_filename)
    startPoint = TOCGenerator.append_TOC(newDoc, generatedDoc, currentTitle, "aLooperTestTOC.pdf", startPoint)
    percentage = round(((index+1) / len(dataStartArray)) * 100)
    print("Document %i percent complete..."%(percentage))



