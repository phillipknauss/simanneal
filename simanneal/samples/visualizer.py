""" Simple tkinter visualizer for 2D data """
""" todo: Refactor to make more reusable """

import threading
from tkinter import *

from simanneal.samples.twodimensional import TwoDimensionalSample

master = Tk()

xMargin = 10
yMargin = 10
width = 200
height = 200
scale = 10

def coordToScreen(coord):
    return coord[0] * scale + xMargin, coord[1] * scale + yMargin

def drawAxes():
    w.create_line(xMargin, yMargin, xMargin, height-yMargin)
    w.create_line(xMargin,yMargin, width-xMargin, yMargin)

def drawMarks():
    for i in range(xMargin, width-xMargin, 10):
        pt1 = xMargin+i, 0
        pt2 = xMargin+i, yMargin
        w.create_line(pt1[0],pt1[1],pt2[0],pt2[1])
    for i in range(yMargin, height-yMargin, 10):
        pt1 = 0, yMargin+i
        pt2 = xMargin, yMargin+i
        w.create_line(pt1[0],pt1[1],pt2[0],pt2[1])

def drawCoords(coords):
    for i in range(len(coords)-1):
        pos1 = coordToScreen(coords[i])
        pos2 = coordToScreen(coords[i+1])
        w.create_line(pos1[0],pos1[1],pos2[0],pos2[1])

def anneal():
    optimized = sample.run()
    coords = optimized["bestState"]
    drawCoords(coords)
    lText.set("Done")

def anneal_threaded():
    t = threading.Thread(target=anneal)
    t.setDaemon(True)
    t.start()

def clear():
    w.delete(ALL)
    drawAxes()
    drawMarks()

def updateProgress(status):
    lText.set((status["count"]/10000)*100)
    
def buildUI():
    global w
    w = Canvas(master, width=200, height=200)
    w.pack()

    global b
    b = Button(master, text="Anneal", command=anneal_threaded)
    b.pack()

    global b2
    b2 = Button(master, text="Clear", command=clear)
    b2.pack()

    global l
    global lText
    lText = StringVar()
    l = Label(master, textvariable=lText)
    l.pack()

buildUI()
sample = TwoDimensionalSample()
sample.reportPeriod = 500
sample.reportFunction = updateProgress
clear()
mainloop()
