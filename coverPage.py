import fitz

def createCoverPage(event, clustering):
    
    #SETTING UP
    doc = fitz.open()
    page = doc.newPage()
    
    #FORMATTING
    headerRect = fitz.Rect(70, 200, 500, 700)
    subHeaderRect = fitz.Rect(70, 260, 500, 700)
    namesRect = fitz.Rect(70, 400, 500, 700)
    
    #TEXT
    header = event
    subHeader = clustering
    namesText = "Cristian Garces, Bradley Krakar, Jesse Ladyman, Rami Jaber"

    #TEXTBOXES
    rc = page.insertTextbox(headerRect, header,
                        align=fitz.TEXT_ALIGN_CENTER , 
                        fontsize = 40)

    rc = page.insertTextbox(subHeaderRect, subHeader,
                        align=fitz.TEXT_ALIGN_CENTER , 
                        fontsize = 25)
    
    rc = page.insertTextbox(namesRect, namesText,
                        align=fitz.TEXT_ALIGN_CENTER , 
                        fontsize = 15)

    doc.save("title.pdf")

    return doc