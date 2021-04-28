import pandas as pd
import plotly.express as px

# Generates a plot of the given dataset of biometric vs. index and highlights the selected values.
def plotBiometric(data, dataStart, dataEnd, biometric, filename):

    # Adjust dataStart and dataEnd to compensate for time axis
    dataStart = dataStart/500
    dataEnd = dataEnd/500

    rolling = data[biometric].rolling(5000).mean()

    index = data.index
    timeArray = []
    #indexArray = []
    indexPlaceholder = 1

    for item in index:
        setTime = indexPlaceholder / 500
        timeArray.append(setTime)
        indexPlaceholder = indexPlaceholder + 1
        #indexArray.append(item*2)

    fig = px.line(data, x=timeArray, y=rolling,
                  labels={"x": "time (sec)", "y":biometric})
    fig.add_vrect(dataStart, dataEnd, fillcolor="yellow", opacity=0.6)
    fig.write_image(filename)

    return

# Ignore
# def plotBiometricPlain(data, biometric):
#     fig = px.line(data, y=biometric)
#     return fig

# Ignore
# def addHighlightedRegion(plot, dataStart, dataEnd, filename):
#     highlightedPlot = plot
#     highlightedPlot.add_vrect(dataStart, dataEnd, fillcolor="yellow", opacity=0.6)
#     highlightedPlot.write_image(filename)
#     return