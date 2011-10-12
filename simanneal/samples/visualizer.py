""" Simple tkinter visualizer for 2D data """
""" todo: Refactor to make more reusable """

import threading
import time
import pickle
import json
import random
import math
from tkinter import *

from twodimensional import TwoDimensionalSample
import bitmap

global window

def anneal():
    print("anneal")
    window.statusText.set("Annealing...")

    window.sample.maxCount = window.getInt("maxCount")
    window.sample.minEnergy = window.getInt("minEnergy")
    window.sample.reportPeriod = window.getInt("reportPeriod")
    window.sample.alpha = window.getInt("alpha")
    
    optimized = sample.run()
    window.sample.state = optimized["bestState"] # Prime annealer for reuse
    window.update(optimized["bestState"], optimized["bestEnergy"])

def updateProgress(status):
    elapsed = time.clock()
    window.statusText.set("Elapsed: {0:.2f}".format(elapsed-window.timer.lastStart) + "(" + "{0:.2f}".format(status["bestEnergy"]) + ")")
    
    if window.sample.state != status["bestState"]:
        window.sample.state = status["bestState"]
        window.clearCanvas()
        window.drawCoords(status["bestState"])

def improve():
    "Update initialState with candidates until energy improves once"

    print("improve")
    window.statusText.set("Improving...")
    startEnergy = window.sample.E(window.sample.state)
    energy = startEnergy
    while energy >= startEnergy:
        window.sample.state = window.sample.neighbor(window.sample.state)
        energy = sample.E(window.sample.state)
    window.updateUIFromSample()

def parabolic():
    coords = []
    for i in range(-20,20):
        coords.append( (i+100, ((i)*(i))/10+100) )
    window.sample.state = coords
    window.updateUIFromSample()

def cubic():
    coords = []
    for i in range(-20,20):
        coords.append( (i+100, ((i)*(i)*(i))/100+100) )
    window.sample.state = coords
    window.updateUIFromSample()

def randomize():
    "Update State to a random order"

    print("randomize")
    for n in sample.state:
        window.sample.state = window.sample.neighbor(window.sample.state)
    window.updateUIFromSample()  

def import_data():
    print("import")
    with open('data.dat', mode='rb') as file:
        window.sample.state = pickle.load(file)
    window.updateUIFromSample()

def export_data():
    print("export")
    with open('data.dat', mode='wb') as file:
        pickle.dump(window.sample.state, file)
    window.updateUIFromSample()

def export_json():
    print("export_json")
    with open('data.json', mode='w') as file:
        json.dump(window.sample.state, file)
    window.updateUIFromSample()

def import_json():
    with open('data.json', mode='r') as file:
        window.sample.state = json.load(file)
    window.updateUIFromSample()

def export_bitmap():
    print("export_bitmap - not implemented")

def import_bitmap():
    print("import_bitmap")
    window.sample.state = bitmap.imageToData('lena100.bmp', 'data.dat')
    window.updateUIFromSample()

class Timer(object):

    def __init__(self):
        self.lastStart = None
        self.laststop = None
        self.runTime = None
    
    def startClock(self):
        self.lastStart = time.clock()
    
    def stopClock(self):
        if self.lastStart is None:
            return
        self.lastStop = time.clock()
        self.runTime = self.lastStop - self.lastStart
        print("Run duration: ", self.runTime)

class GUI(object):
    def __init__(self, sample):
        self.canvas = Canvas(master, width=200, height=200)
        self.frames = []
        self.settings = []
        self.buttons = []
        self.invertedAvailabilityButtons = []
        self.statusText = StringVar()
        self.statusBar = Label(master, textvariable=self.statusText)
        self.timer = Timer()

        self.sample = sample

    def build(self):
        self.canvas.pack(side=TOP)
        for setting in self.settings:
            setting[1].pack(side=TOP)
        for frame in self.frames:
            frame.pack(side=TOP)
        for button in self.buttons:
            button.pack(side=LEFT)
        self.statusBar.pack(side=TOP)

    def addFrame(self, name, control):
        self.frames.append(control)
        return control

    def addSetting(self, name, default):
        frame = Frame(master)
        label = Label(frame, text=name)
        entry = Entry(frame)
        entry.insert(0,default)
        label.pack(side=LEFT)
        entry.pack(side=LEFT)
        self.settings.append( (name,frame,label,entry) )
        return frame

    def getSettingValue(self, name):
        
        matches = [ item for item in self.settings if item[0]==name ]
        return matches[0][3].get()

    def getInt(self, name):
        return int(self.getSettingValue(name))

    def addButton(self, name, control):
        self.buttons.append(control)
        return control

    def enableButtons(self):
        for b in self.buttons:
            if b in self.invertedAvailabilityButtons:
                b.config(state=DISABLED)
            else:
                b.config(state=NORMAL)

    def disableButtons(self):
        for b in self.buttons:
            if b in self.invertedAvailabilityButtons:
                b.config(state=NORMAL)
            else:
                b.config(state=DISABLED)
                

    def run_threaded(self, function):
        thread = threading.Thread(target=function)
        thread.setDaemon(True) # kills the thread if parent thread is killed
        self.timer.startClock()
        thread.start()
        self.disableButtons()

    def stop_thread(self):
        # This sometimes crashes the python runtime... needs to be fixed
        self.sample.stop()
        self.updateUIFromSample()

    def clearCanvas(self):
        self.canvas.delete(ALL)
        self.drawAxes()
        self.drawMarks()

    def coordToScreen(self, coord):
        xMargin = window.getInt("xMargin")
        yMargin = window.getInt("yMargin")
        height = window.getInt("height")
        width = window.getInt("width")
        scale = window.getInt("scale")
        return coord[0] * scale + xMargin, coord[1] * scale + yMargin

    def drawAxes(self):
        xMargin = window.getInt("xMargin")
        yMargin = window.getInt("yMargin")
        height = window.getInt("height")
        width = window.getInt("width")
        self.canvas.create_line(xMargin, yMargin, xMargin, height-yMargin)
        self.canvas.create_line(xMargin,yMargin, width-xMargin, yMargin)

    def drawMarks(self):
        xMargin = window.getInt("xMargin")
        yMargin = window.getInt("yMargin")
        height = window.getInt("height")
        width = window.getInt("width")
        for i in range(xMargin, width-xMargin, 10):
            pt1 = xMargin+i, 0
            pt2 = xMargin+i, yMargin
            self.canvas.create_line(pt1[0],pt1[1],pt2[0],pt2[1])
        for i in range(yMargin, height-yMargin, 10):
            pt1 = 0, yMargin+i
            pt2 = xMargin, yMargin+i
            self.canvas.create_line(pt1[0],pt1[1],pt2[0],pt2[1])

    def drawCoords(self,coords):
        if coords is int:
            return;
        for i in range(len(coords)-1):
            pos1 = self.coordToScreen(coords[i])
            pos2 = self.coordToScreen(coords[i+1])
            try:
                self.canvas.create_line(pos1[0],pos1[1],pos2[0],pos2[1])
            except:
                print("Failed to draw line from ", (pos1[0],pos1[1]), "to", (pos2[0],pos2[1]))

    def update(self, state, energy):
        self.timer.stopClock()
        self.clearCanvas()
        self.drawCoords(state)
        self.statusText.set("New energy: " + "{0:.2f}".format(energy))

        self.enableButtons()

    def updateUIFromSample(self):
        self.update(self.sample.state, self.sample.E(self.sample.state))   
    
def buildUI(sample):
    
    window = GUI(sample)
    print("preControls")
    
    window.addSetting("xMargin","10")
    window.addSetting("yMargin","10")
    window.addSetting("width","200")
    window.addSetting("height","200")
    window.addSetting("scale","1")

    window.addSetting("maxCount","1000000")
    window.addSetting("minEnergy","850")
    window.addSetting("reportPeriod","1000")
    window.addSetting("alpha","1")
    
    f0 = window.addFrame("data_import_export", Frame(master))
    window.addButton("import", Button(f0, text="Import Data", command=lambda : window.run_threaded(import_data)))
    window.addButton("export", Button(f0, text="Export Data", command=lambda : window.run_threaded(export_data)))
    f1 = window.addFrame("json_import_export", Frame(master))
    window.addButton("import_json", Button(f1, text="Import JSON", command=lambda : window.run_threaded(import_json)))
    window.addButton("export_json", Button(f1, text="Export JSON", command=lambda : window.run_threaded(export_json)))
    f2 = window.addFrame("generators", Frame(master))
    window.addButton("parabolic", Button(f2, text="Parabolic", command=lambda : window.run_threaded(parabolic)))
    window.addButton("cubic", Button(f2, text="Cubic", command=lambda : window.run_threaded(cubic)))
    window.addButton("random", Button(f2, text="Random", command=lambda : window.run_threaded(randomize)))
    f3 = window.addFrame("actions", Frame(master))
    window.addButton("anneal", Button(f3, text="Anneal", command=lambda : window.run_threaded(anneal)))
    window.addButton("improve", Button(f3, text="Improve", command=lambda : window.run_threaded(improve)))
    stopButton = Button(f3, text="Stop", command=window.stop_thread, state=DISABLED)
    window.addButton("stop", stopButton)
    window.invertedAvailabilityButtons.append(stopButton)
    print("preBuild")
    window.build()
    print("postBuild")
    return window
    

def genRandom(count):
    initialState = []
    for i in range(0,100):
        x, y = random.randint(0,180), random.randint(0,180)
        initialState.append( (x,y) )

    window.sample.state = initialState
    window.updateUIFromSample()

sample = TwoDimensionalSample()
sample.reportFunction = updateProgress

print("here-1")

global master
master = Tk()
window = buildUI(sample)

print("here1")
window.clearCanvas()
print("here2")

genRandom(100)

master.mainloop()
