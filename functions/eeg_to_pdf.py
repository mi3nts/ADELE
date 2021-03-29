import eeg_viz as eeg
import pandas as pd
import fitz


def createRow(data, doc, rowNum, start, end):
    eeg.eeg_viz(data,start,end,"eeg"+str(rowNum))
    
    page=rowNum//3            #Make sure first rowNum is 0
    if(rowNum%3==0):
        doc.insert_page(page)
    
    offset=rowNum%3*300
        
    doc[page].insert_text((50,20+offset),"Alpha of %i:%i"%(start,end))
    doc[page].insert_text((250,20+offset),"Beta of %i:%i"%(start,end))
    doc[page].insert_text((450,20+offset),"Theta of %i:%i"%(start,end))
    doc[page].insert_image(fitz.Rect(0, 30+offset, 200, 230+offset),filename=("eeg"+str(rowNum)+"alpha.png"))
    doc[page].insert_image(fitz.Rect(200, 30+offset, 400, 230+offset),filename=("eeg"+str(rowNum)+"beta.png"))
    doc[page].insert_image(fitz.Rect(400, 30+offset, 600, 230+offset),filename=("eeg"+str(rowNum)+"theta.png"))



def createDoc(data,doc,vals): #vals as a list of tuples of start and end numbers
    i=0
    for value in vals:
        createRow(data,doc,i,value[0],value[1])
        i+=1






data=pd.read_csv('2020_06_04_T05_U00T_ADELE.csv')

doc=fitz.open()

#createDoc(data,doc,[(1000,2000),(2000,3000),(3000,4000),(4000,5000),(5000,6000),(6000,70000),(7000,8000),(8000,9000),(9000,10000)])

createDoc(data,doc,[(10000,20000),(50000,60000),(90000,100000)])

doc.save("eeg_heatmaps.pdf")