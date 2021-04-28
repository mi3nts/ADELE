import fitz
from fitz import Rect
from fitz.utils import getColor
import pandas as pd
import docGenerator

# This function takes an existing document and adds a Table of Contents page as the first page
def generateTOC(existingDoc, filename):
    generatedPage = existingDoc.newPage(pno=0)

    # Generates the Table of Contents Title
    tableOfContentsText = "-- Table of Contents --"
    TOC_textLength = fitz.getTextlength(tableOfContentsText)
    TOC_startPoint_X = ((595 / 2) - TOC_textLength)
    TOC_startPoint_Y = 85
    TOC_startPoint = fitz.Point(TOC_startPoint_X, TOC_startPoint_Y)
    generatedPage.insertText(TOC_startPoint, tableOfContentsText, fontname="Times-Roman", color=(0, 0.35, 0.8),
                             fontsize=24, rotate=0)

    # Inserts the page number at the bottom of the page.
    # Table of Contents will be page 1
    pageNumberPoint = fitz.Point(294, 815)
    generatedPage.insertText(pageNumberPoint, "1", fontname="Times-Roman", fontsize=14, rotate=0)
    existingDoc.save(filename)

    return existingDoc

# This function inserts a new page to the document and creates an entry for it in the table of contents.
# existingDoc is the document that contains the table of contents, newDoc is the document that will be appended,
# entryname is the title of the appended document, and filename is what the combined document will be saved as
# startPoint is the location on the TOC page where the next entry will begin
# For this function to work properly, the first page in existingDoc must be the table of contents
# This function also inserts the page numbers at the bottom of all appended pages
# This function returns the startPoint for the next entry that will be appended
def append_TOC(existingDoc, newDoc, entryname, filename, startPoint):

    # Appends the new page to the existing document that contains the table of contents
    existingDoc.insert_pdf(newDoc)
    TOC_page = existingDoc.load_page(page_id=0)

    # Generates the text entry for the new page
    TOC_page.insertText(startPoint, entryname, fontname="helv", fontsize=16, rotate=0)
    x_distance = (fitz.getTextlength(entryname, fontname="helv", fontsize=16)) + 105
    targetPageNumber = existingDoc.page_count
    entrynumber = "   %i" % targetPageNumber
    while(x_distance < 475):
        dotLocation = fitz.Point(x_distance, startPoint.y)
        TOC_page.insertText(dotLocation, ".", fontname="helv", fontsize=16, rotate=0)
        x_distance = x_distance + 5
    TOC_page.insertText(dotLocation, entrynumber, fontname="helv", fontsize=16, rotate=0)

    # Creates the hyperlink for the newly appended page
    # When the entry is clicked on in the Table of Contents, user is sent to that particular page
    linkRect = Rect(100, startPoint.y-20, x_distance + 25, startPoint.y + 15)
    newLink = TOC_page.insert_link({'kind': 1, 'from': linkRect, 'type': 'goto', 'page': targetPageNumber-1, 'to': fitz.Point(0, 0), 'zoom': 0.0})

    # Inserts the page number on the bottom of the newly appended page
    insertedPage = existingDoc.load_page(page_id=-1)
    pageNumberPoint = fitz.Point(294, 830)
    insertPageNumber = "%i" % targetPageNumber
    insertedPage.insertText(pageNumberPoint, insertPageNumber, fontname="Times-Roman", fontsize=14, rotate=0)

    # Calculates the new start point for the next entry and saves the pdf
    newStartPoint = fitz.Point(100, startPoint.y + 35)
    existingDoc.save(filename)

    return newStartPoint

# Appends the cover page to the finished document
# This should be the last page to be appended
def append_CoverPage(reportDoc, coverpageDoc, filename):

    reportDoc.insert_pdf(coverpageDoc, start_at=0)
    reportDoc.save(filename)