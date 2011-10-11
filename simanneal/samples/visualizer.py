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
    clear()
    lText.set("Final energy:" + "{0:.2f}".format(optimized["bestEnergy"]))

def run_threaded(function):
    t = threading.Thread(target=function)
    t.setDaemon(True) # kills the thread if parent thread is killed
    t.start()
    b.config(state=DISABLED)
    b2.config(state=DISABLED)
    b3.config(state=DISABLED)

def anneal_threaded():
    run_threaded(anneal)

def clear():
    w.delete(ALL)
    drawAxes()
    drawMarks()

def updateProgress(status):
    lText.set("{0:.2f}".format((status["count"]/maxCount)*100))

def updateUIFromSample():
    clear()
    drawCoords(sample.state)
    lText.set("New energy: " + "{0:.2f}".format((sample.E(sample.state))))
    b.config(state=NORMAL)
    b2.config(state=NORMAL)
    b3.config(state=NORMAL)

def improve():
    "Update initialState with candidates until energy improves once"

    lText.set("Improving...")
    startEnergy = sample.E(sample.state)
    energy = startEnergy
    while energy >= startEnergy:
        sample.state = sample.neighbor(sample.state)
        energy = sample.E(sample.state)
    updateUIFromSample()

def improve_threaded():
    run_threaded(improve)

def randomize():
    "Update State to a random order"

    for n in sample.state:
        sample.state = sample.neighbor(sample.state)
    updateUIFromSample()  

def randomize_threaded():
    run_threaded(randomize)

def buildUI():
    global w
    w = Canvas(master, width=200, height=200)
    w.pack(side=TOP)

    global f
    f = Frame(master)
        
    global b
    b = Button(f, text="Anneal", command=anneal_threaded)
    b.pack(side=LEFT)

    global b2
    b2 = Button(f, text="Improve", command=improve_threaded)
    b2.pack(side=LEFT)

    global b3
    b3 = Button(f, text="Randomize", command=randomize_threaded)
    b3.pack(side=LEFT)

    f.pack(side=TOP)

    global l
    global lText
    lText = StringVar()
    l = Label(master, textvariable=lText)
    l.pack(side=TOP)

def drawInitialState(coords):
    """ Separate function so we can apply color or something differently """

    drawCoords(coords);

buildUI()
clear()
global sample
sample = TwoDimensionalSample()
# This is where we set the data
#initialState = [(0,12), (1,2), (2,14), (3,0), (4,5), (5,13), (6,6), (7,8), (8,3), (9,10), (10,4), (11,11), (12,7), (13,9), (14,1)];
initialState = [(0,4), (1,3), (2,2), (3,1), (4,0), (5,1), (6,2), (7,3), (8,4), (9,3), (10,2), (11,1), (12,0), (13,1), (14,2), (15,3), (16,4)];
sample.state = initialState
drawInitialState(sample.state);
lText.set("Initial energy: " + "{0:.2f}".format(sample.E(sample.state)))
global maxCount
maxCount = 1000000
sample.maxCount = maxCount
sample.reportPeriod = maxCount/100
sample.reportFunction = updateProgress

""" alpha determines how quickly the temperature falls off
With a small data set with few or no local minima that are not global minima, set this high to find results quickly
With a large data set which may have local non-global minima, set this low to allow more time be able to step backwards """ 
sample.alpha = 0.9 # Temp should fall off quickly

mainloop()
