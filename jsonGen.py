from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import Image, ImageTk
from os import listdir
import json

if __name__ == "__main__":
    firstX = 0
    firstY = 0
    sX = 0
    sY = 0
    tX = 0
    tY = 0
    
    root = Tk()
    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)

    
    dirFiles = listdir(".")
    dirImageFiles = []
    for f in dirFiles:
        if f.endswith(".jpg"):
            dirImageFiles.append(f)    
    
    for File in dirImageFiles:
        clicks = 0
        fout = open(File.strip(".jpg")+".json","w")        
        #adding the image        
        #File = askopenfilename(parent=root, initialdir="C:/Users/Raghu/Desktop",title='Choose an image.')
        img = ImageTk.PhotoImage(Image.open(File))
        canvas.create_image(0,0,image=img,anchor="nw")
        canvas.config(scrollregion=canvas.bbox(ALL))

        #function to be called when mouse is clicked
        def printcoords(event):
            #outputting x and y coords to console
            global clicks, root, firstX, firstY, sX, sY, tX, tY, outputFile
            canvas = event.widget
            print (canvas.canvasx(event.x),canvas.canvasy(event.y))
            clicks += 1
            if clicks == 1:
                firstX = canvas.canvasx(event.x)
                firstY = canvas.canvasy(event.y)
            elif clicks == 2:
                sX = canvas.canvasx(event.x)
                sY = canvas.canvasy(event.y)
            elif clicks == 3:
                tX = canvas.canvasx(event.x)
                tY = canvas.canvasy(event.y)
            elif clicks >=4:                
                points = '{"x":%s, "y":%s, "w":%s, "h":%s, "bx":%s, "by":%s, "bw":%s, "bh":%s}'%(firstX,
                                                                                                 firstY,
                                                                                                 sX-firstX,
                                                                                                 sY-firstY,
                                                                                                 tX, tY,
                                                                                                 canvas.canvasx(event.x)-tX,
                                                                                                 canvas.canvasy(event.y)-tY
                                                                                                 )
                #.format(firstX,firstY)
                #'[{"x":firstX," y":firstY, "w":sX-firstX, "h":sY-firstY,\
                #          "px":tX, "py":tY, "pw":event.x-tX, "ph":event.y-tY}]'
                #points = '["foo", {"bar":["baz", null, 1.0, 2]}]'
                parsed = json.loads(points)
                fout.write(json.dumps(parsed, indent = 2))
                fout.close()
                root.quit()
                
            
        #mouseclick event
        canvas.bind("<Button 1>",printcoords)
        root.mainloop()        
        
        
            

        
