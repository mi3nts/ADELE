import pandas as pd
import plotly.express as px

# Generates a plot of the given dataset of biometric vs. index and highlights the selected values.
def plotBiometric(data, dataStart, dataEnd, biometric, filename):

    # Adjust dataStart and dataEnd to compensate for time axis
    dataStart = dataStart/500
    dataEnd = dataEnd/500

    index = data.index
    timeArray = []
    #indexArray = []
    indexPlaceholder = 1

    for item in index:
        setTime = indexPlaceholder / 500
        timeArray.append(setTime)
        indexPlaceholder = indexPlaceholder + 1
        #indexArray.append(item*2)

    fig = px.line(data, x=timeArray, y=biometric,
                  labels={"x": "time (sec)"})
    fig.add_vrect(dataStart, dataEnd, fillcolor="yellow", opacity=0.6)
    fig.write_image(filename)

    return

# Ignore
def plotBiometricPlain(data, biometric):
    fig = px.line(data, y=biometric)
    return fig

# Ignore
def addHighlightedRegion(plot, dataStart, dataEnd, filename):
    highlightedPlot = plot
    highlightedPlot.add_vrect(dataStart, dataEnd, fillcolor="yellow", opacity=0.6)
    highlightedPlot.write_image(filename)
    return

# Test Code

# data = pd.read_csv('2020_06_04_T05_U00T_ADELE.csv')
# dataStart = 50000
# dataEnd = 60000
# biometric = "HR"
# filename = "atestPlot2.png"
# plotBiometric(data, dataStart, dataEnd, biometric, filename)
# #plotBiometric(data, 70000, 90000, "HR", "atestPlot3.png")