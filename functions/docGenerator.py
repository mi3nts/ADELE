import pandas as pd
import fitz
import cv2
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from fitz import Rect

# Creates a new blank PDF
doc = fitz.open()
generatedPage = doc.newPage()

# Prints the dimensions of the newly generated page.
# These values may be useful for determining the locations of the plots
pageRect = generatedPage.bound()
pageArea = pageRect.getArea()
page_x0 = pageRect.x0
page_y0 = pageRect.y0
page_x1 = pageRect.x1
page_y1 = pageRect.y1
print("Page X0 = ", page_x0)
print("Page Y0 = ", page_y0)
print("Page X1 = ", page_x1)
print("Page Y1 = ", page_y1)

# Generates the placeholder images on the pdf

heatmapPlaceholder1 = fitz.Rect(10, 10, 198, 275)
generatedPage.insertImage(heatmapPlaceholder1, filename="heatmapPlaceholder.png", keep_proportion=False)

heatmapPlaceholder2 = fitz.Rect(203, 10, 391, 275)
generatedPage.insertImage(heatmapPlaceholder2, filename="heatmapPlaceholder.png", keep_proportion=False)

heatmapPlaceholder3 = fitz.Rect(396, 10, 585, 275)
generatedPage.insertImage(heatmapPlaceholder3, filename="heatmapPlaceholder.png", keep_proportion=False)

biometricPlotPlaceholder1 = fitz.Rect(10, 285, 235, 415)
generatedPage.insertImage(biometricPlotPlaceholder1, filename="biometricPlotPlaceholder.png", keep_proportion=False)

biometricPlotPlaceholder2 = fitz.Rect(360, 285, 585, 415)
generatedPage.insertImage(biometricPlotPlaceholder2, filename="biometricPlotPlaceholder.png", keep_proportion=False)

videoframePlaceholder = fitz.Rect(185, 425, 410, 555)
generatedPage.insertImage(videoframePlaceholder, filename="videoFramePlaceholder.jpg", keep_proportion=False)

biometricPlotPlaceholder3 = fitz.Rect(10, 565, 235, 695)
generatedPage.insertImage(biometricPlotPlaceholder3, filename="biometricPlotPlaceholder.png", keep_proportion=False)

biometricPlotPlaceholder4 = fitz.Rect(360, 565, 585, 695)
generatedPage.insertImage(biometricPlotPlaceholder4, filename="biometricPlotPlaceholder.png", keep_proportion=False)

textPlaceholder = fitz.Rect(10, 705, 585, 832)
generatedPage.insertImage(textPlaceholder, filename="textPlaceholder.png", keep_proportion=False)

# Saves the PDF
doc.save("aGeneratedDoc.pdf")