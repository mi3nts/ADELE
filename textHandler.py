import fitz
from fitz.utils import getColor

# Calculates the percent increase between a smaller number and a larger number
def calculatePercentIncrease(largerNum, smallerNum):
    difference = largerNum - smallerNum
    percentIncrease = difference / smallerNum
    return percentIncrease

# Generates the textbox for each page
# Checks to make sure that the text will fit inside the textbox and
# reduces font size as needed.
def createTextbox(textfile, textboxRect, page):

    fontSize = 12
    linecounter = 0

    # Extracts text from file and eliminates blank lines
    # Counts the number of lines in the file
    with open(textfile) as input_txt:
        lineString = ""
        lineArray = []
        for line in input_txt:
            if not line.isspace():
                lineString = lineString + line
                lineArray.append(line)
                linecounter = linecounter + 1
                lineLength = fitz.getTextlength(line, "Times-Roman", fontSize)
                while (lineLength > textboxRect.width):
                    linecounter = linecounter + 1
                    lineLength = lineLength - textboxRect.width

    # At font size 12, textbox can hold up to 10 lines of text
    # Decreases font size by increments of 4 while line capacity is exceeded
    lineCapacity = 10
    while(linecounter > lineCapacity):

        # Line capacity of textbox increases by the percent increase from each font size decrement
        # Ex: 12 --> 8 makes for a 50% increase in line capacity
        percentIncrease = calculatePercentIncrease(fontSize, fontSize-2)
        lineCapacity = lineCapacity + (lineCapacity * percentIncrease)

        # Decrement font size by increment of 2
        fontSize = fontSize - 2
        linecounter = 0

        # Recalculate the number of lines
        # This is necessary since decreasing font size may decrease the number of lines
        # When text exceeds horizontal boundaries, a new line is started
        for line in lineArray:
            linecounter = linecounter + 1
            lineLength = fitz.getTextlength(line, "Times-Roman", fontSize)
            while(lineLength > textboxRect.width):
                linecounter = linecounter + 1
                lineLength = lineLength - textboxRect.width

    # Generate textbox with text
    textboxShape = page.new_shape()
    textboxShape.draw_rect(textboxRect)
    textboxShape.finish(color=getColor("dodgerblue4"), fill_opacity=1, closePath=False)
    textboxShape.commit()
    page.insertTextbox(textboxRect, lineString, fontsize=fontSize, fontname="Times-Roman", align=0)

    return