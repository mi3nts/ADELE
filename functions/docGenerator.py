import fitz
from fitz import Rect

# This function autogenerates a document given three heatmaps, four biometric plots, and a video frame with space for text at the bottom.
# This function requires a title, the images of all heatmaps and bio plots, the text to be included, and the filename/location where
# the document will be saved.
def generateDoc(title, heatmap1, heatmap2, heatmap3, bio1, bio2, bio3, bio4, vidFrame, text, filename):

    # Creates a new blank PDF
    doc = fitz.open()
    generatedPage = doc.newPage()

    font = "Times-Roman"
    fontSize = 24
    titleLength = fitz.getTextlength(titleText, font, fontSize)

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

    # Generates the placeholder images on the pdf

    heatmap1_Location = fitz.Rect(10, 50, 198, 315)
    generatedPage.insertImage(heatmap1_Location, filename=heatmap1, keep_proportion=False)

    heatmap2_Location = fitz.Rect(203, 50, 391, 315)
    generatedPage.insertImage(heatmap2_Location, filename=heatmap2, keep_proportion=False)

    heatmap3_Location = fitz.Rect(396, 50, 585, 315)
    generatedPage.insertImage(heatmap3_Location, filename=heatmap3, keep_proportion=False)

    bio1_Location = fitz.Rect(10, 325, 235, 455)
    generatedPage.insertImage(bio1_Location, filename=bio1, keep_proportion=False)

    bio2_Location = fitz.Rect(360, 325, 585, 455)
    generatedPage.insertImage(bio2_Location, filename=bio2, keep_proportion=False)

    vidFrame_Location = fitz.Rect(185, 465, 410, 595)
    generatedPage.insertImage(vidFrame_Location, filename=vidFrame, keep_proportion=False)

    bio3_Location = fitz.Rect(10, 605, 235, 735)
    generatedPage.insertImage(bio3_Location, filename=bio3, keep_proportion=False)

    bio4_Location = fitz.Rect(360, 605, 585, 735)
    generatedPage.insertImage(bio4_Location, filename=bio4, keep_proportion=False)

    text_Location = fitz.Rect(10, 745, 585, 815)
    generatedPage.insertImage(text_Location, filename=text, keep_proportion=False)

    # Saves the PDF
    doc.save(filename)

    return doc

# Testing the document autogenerator
titleText = "TITLE PLACEHOLDER"
heatmapPlaceholder = "heatmapPlaceholder.png"
bioPlotPlaceholder = "biometricPlotPlaceholder.png"
vidFramePlaceholder = "videoFramePlaceholder.jpg"
textPlaceholder = "textPlaceholder.png"
filename = "aGeneratedDoc.pdf"
generatedDoc = generateDoc(titleText, heatmapPlaceholder, heatmapPlaceholder, heatmapPlaceholder, bioPlotPlaceholder, bioPlotPlaceholder,
                           bioPlotPlaceholder, bioPlotPlaceholder, vidFramePlaceholder,textPlaceholder, filename)
print("Document successfully generated!")

