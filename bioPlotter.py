import pandas as pd
import plotly.express as px
# import plotly.graph_objects as go

# Generates a plot of the given dataset of biometric vs. index and highlights the selected values.
def plotBiometric(data, dataStart, dataEnd, biometric, filename):

    # fig = go.Figure()
    # fig.add_trace(go.Scatter(data, y=biometric+5000))
    rolling = data[biometric].rolling(5000).mean()


    fig = px.line(data, y=rolling)
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
# plotBiometric(data, 70000, 90000, "HR", "atestPlot3.png")