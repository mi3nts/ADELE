import fitz
from fitz import Rect
import matplotlib.pyplot as plt
import pandas as pd
import eeg_viz as eeg
import extractFrame as vidFrame
import bioPlotter
from fitz.utils import getColor
import textHandler

# This function autogenerates a document given three heatmaps, four biometric plots, and a video frame with space for text at the bottom.
# This function requires a title, the images of all heatmaps and bio plots, the text to be included, and the filename/location where
# the document will be saved.
def generateDoc(title, data, dataStart, dataEnd, bio1, bio2, bio3, bio4, vid_filename, textfile, filename, pageNum, path):

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
    bio1_filename = path + "page%i_"% pageNum + bio1 + ".png"
    bioPlotter.plotBiometric(data, dataStart, dataEnd, bio1, bio1_filename)

    bio2_filename = path + "page%i_"% pageNum + bio2 + ".png"
    bioPlotter.plotBiometric(data, dataStart, dataEnd, bio2, bio2_filename)


    bio3_filename = path + "page%i_"% pageNum + bio3 + ".png"
    bioPlotter.plotBiometric(data, dataStart, dataEnd, bio3, bio3_filename)


    bio4_filename = path + "page%i_"% pageNum + bio4 + ".png"
    bioPlotter.plotBiometric(data, dataStart, dataEnd, bio4, bio4_filename)

    # Autogenerates the EEG heatmaps
    eeg.eeg_viz(data, dataStart, dataEnd, path + "page%i_eeg_"% pageNum)
    fontSize = 14

    # Extracts a frame from the video in the specified time range
    extracted_frame_filename = path + "page%i_extracted_frame.jpg"% pageNum
    vidFrame.extractFrame(vid_filename, dataStart, dataEnd, extracted_frame_filename)

    # Inserts heatmap visualizations
    heatmapAlpha_Location = fitz.Rect(10, 50, 198, 238)
    generatedPage.insertImage(heatmapAlpha_Location, filename=path + "page%i_eeg_alpha.png"% pageNum, keep_proportion=False)
    alphaText = "Alpha Band"
    textLength = fitz.getTextlength(alphaText, font, fontSize)
    startPoint = fitz.Point(((10 + 94) - textLength/2), 240)
    generatedPage.insertText(startPoint, alphaText, fontname=font, fontsize=fontSize, rotate=0)

    heatmapBeta_Location = fitz.Rect(203, 50, 391, 238)
    generatedPage.insertImage(heatmapBeta_Location, filename=path + "page%i_eeg_beta.png"% pageNum, keep_proportion=False)
    betaText = "Beta Band"
    textLength = fitz.getTextlength(alphaText, font, fontSize)
    startPoint = fitz.Point(((203 + 94) - textLength / 2), 240)
    generatedPage.insertText(startPoint, betaText, fontname=font, fontsize=fontSize, rotate=0)

    heatmapTheta_Location = fitz.Rect(396, 50, 585, 238)
    generatedPage.insertImage(heatmapTheta_Location, filename=path + "page%i_eeg_theta.png"% pageNum, keep_proportion=False)
    thetaText = "Theta Band"
    textLength = fitz.getTextlength(alphaText, font, fontSize)
    startPoint = fitz.Point(((396 + 94) - textLength / 2), 240)
    generatedPage.insertText(startPoint, thetaText, fontname=font, fontsize=fontSize, rotate=0)

    # Inserts biometric plots
    bio3_Location = fitz.Rect(10, 443, 300, 653)
    generatedPage.insertImage(bio3_Location, filename=bio3_filename, keep_proportion=False)

    bio4_Location = fitz.Rect(305, 443, 595, 653)
    generatedPage.insertImage(bio4_Location, filename=bio4_filename, keep_proportion=False)

    bio1_Location = fitz.Rect(10, 253, 300, 463)
    generatedPage.insertImage(bio1_Location, filename=bio1_filename, keep_proportion=False)

    bio2_Location = fitz.Rect(305, 253, 595, 463)
    generatedPage.insertImage(bio2_Location, filename=bio2_filename, keep_proportion=False)

    # Generates textbox
    textboxBack_Location = fitz.Rect(250, 650, 585, 815)
    textHandler.createTextbox(textfile, textboxBack_Location, generatedPage, path)

    # Inserts video frame
    vidFrame_Location = fitz.Rect(25, 675, 245, 799)
    generatedPage.insertImage(vidFrame_Location, filename=extracted_frame_filename, keep_proportion=False)

    # Saves the PDF -- not needed anymore
    #doc.save(filename)

    return doc