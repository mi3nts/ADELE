import fitz
from fitz import Rect
import matplotlib.pyplot as plt
import pandas as pd
import eeg_viz as eeg
import extractFrame as vidFrame
import bioPlotter

# This function autogenerates a document given three heatmaps, four biometric plots, and a video frame with space for text at the bottom.
# This function requires a title, the images of all heatmaps and bio plots, the text to be included, and the filename/location where
# the document will be saved.
def generateDoc(title, data, dataStart, dataEnd, bio1, bio2, bio3, bio4, vid_filename, text, filename):

    # Creates a new blank PDF
    doc = fitz.open()
    generatedPage = doc.newPage()

    font = "Times-Roman"
    fontSize = 24
    titleLength = fitz.getTextlength(title, font, fontSize)

    # Prints the dimensions of the newly generated page.
    # These values may be useful for determining the locations of the plots
    pageRect = generatedPage.bound()
    page_x0 = pageRect.x0
    page_x1 = pageRect.x1

    # Ensures that the title will always be centered, despite text length
    pageMidpoint_X = (page_x1 - page_x0) / 2
    titleStartPoint_X = pageMidpoint_X - (titleLength / 2)
    titleStartPoint_Y = fontSize + 11
    titleStartPoint = fitz.Point(titleStartPoint_X, titleStartPoint_Y)
    generatedPage.insertText(titleStartPoint, title, fontname=font, fontsize=fontSize, rotate=0)

    # Autogenerates the biometric plots
    bio1_filename = "bio1.png"
    bioPlotter.plotBiometric(data, dataStart, dataEnd, bio1, bio1_filename)
    #bioPlotter.addHighlightedRegion(bio1_plotbase, dataStart, dataEnd, bio1_filename)

    bio2_filename = "bio2.png"
    bioPlotter.plotBiometric(data, dataStart, dataEnd, bio2, bio2_filename)
   # bioPlotter.addHighlightedRegion(bio2_plotbase, dataStart, dataEnd, bio2_filename)


    bio3_filename = "bio3.png"
    bioPlotter.plotBiometric(data, dataStart, dataEnd, bio3, bio3_filename)
    #bioPlotter.addHighlightedRegion(bio3_plotbase, dataStart, dataEnd, bio3_filename)


    bio4_filename = "bio4.png"
    bioPlotter.plotBiometric(data, dataStart, dataEnd, bio4, bio4_filename)
    #bioPlotter.addHighlightedRegion(bio4_plotbase, dataStart, dataEnd, bio4_filename)



    # Autogenerates the EEG heatmaps
    eeg.eeg_viz(data, dataStart, dataEnd, "eeg_")
    fontSize = 14

    # Extracts a frame from the video in the specified time range
    extracted_frame_filename = "extracted_frame.jpg"
    vidFrame.extractFrame(vid_filename, dataStart, dataEnd, extracted_frame_filename)

    # Generates the placeholder images on the pdf

    heatmapAlpha_Location = fitz.Rect(10, 50, 198, 238)
    generatedPage.insertImage(heatmapAlpha_Location, filename="eeg_alpha.png", keep_proportion=False)
    alphaText = "Alpha Band"
    textLength = fitz.getTextlength(alphaText, font, fontSize)
    startPoint = fitz.Point(((10 + 94) - textLength/2), 240)
    generatedPage.insertText(startPoint, alphaText, fontname=font, fontsize=fontSize, rotate=0)

    heatmapBeta_Location = fitz.Rect(203, 50, 391, 238)
    generatedPage.insertImage(heatmapBeta_Location, filename="eeg_beta.png", keep_proportion=False)
    betaText = "Beta Band"
    textLength = fitz.getTextlength(alphaText, font, fontSize)
    startPoint = fitz.Point(((203 + 94) - textLength / 2), 240)
    generatedPage.insertText(startPoint, betaText, fontname=font, fontsize=fontSize, rotate=0)

    heatmapTheta_Location = fitz.Rect(396, 50, 585, 238)
    generatedPage.insertImage(heatmapTheta_Location, filename="eeg_theta.png", keep_proportion=False)
    thetaText = "Theta Band"
    textLength = fitz.getTextlength(alphaText, font, fontSize)
    startPoint = fitz.Point(((396 + 94) - textLength / 2), 240)
    generatedPage.insertText(startPoint, thetaText, fontname=font, fontsize=fontSize, rotate=0)

    bio3_Location = fitz.Rect(10, 443, 300, 653)
    generatedPage.insertImage(bio3_Location, filename=bio3_filename, keep_proportion=False)

    bio4_Location = fitz.Rect(305, 443, 595, 653)
    generatedPage.insertImage(bio4_Location, filename=bio4_filename, keep_proportion=False)

    bio1_Location = fitz.Rect(10, 253, 300, 463)
    generatedPage.insertImage(bio1_Location, filename=bio1_filename, keep_proportion=False)

    bio2_Location = fitz.Rect(305, 253, 595, 463)
    generatedPage.insertImage(bio2_Location, filename=bio2_filename, keep_proportion=False)

    text_Location = fitz.Rect(250, 655, 585, 820)
    generatedPage.insertImage(text_Location, filename=text, keep_proportion=False)

    vidFrame_Location = fitz.Rect(25, 675, 245, 799)
    generatedPage.insertImage(vidFrame_Location, filename=extracted_frame_filename, keep_proportion=False)

    # Saves the PDF
    doc.save(filename)

    return doc

# Testing the document autogenerator

# data=pd.read_csv('2020_06_04_T05_U00T_ADELE.csv')
# dataStart = 10000
# dataEnd = 60000
#
# titleText = "TITLE PLACEHOLDER"
# bioPlotPlaceholder = "biometricPlotPlaceholder.png"
# bio1 = "HR"
# bio2 = "Temp"
# bio3 = "AveragePupilDiameter"
# bio4 = "GSR_uS"
# vidFramePlaceholder = "videoFramePlaceholder.jpg"
# textPlaceholder = "textPlaceholder.png"
# vid_filename = "fullstream.mp4"
# filename = "aGeneratedDoc.pdf"
# bioPlotter.plotBiometric(data, dataStart, dataEnd, "Temp", "anewbioplot.png")
# generatedDoc = generateDoc(titleText, data, dataStart, dataEnd, bio1, bio2,
#                            bio3, bio4, vid_filename, textPlaceholder, filename)
# print("Document successfully generated!")
#
