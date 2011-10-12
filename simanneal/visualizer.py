import threading
import time
import pickle
import json
import random
import math
from tkinter import *

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
    def __init__(self, application):
        self.application = application
        application.window = self
        self.canvas = Canvas(master, width=200, height=200)
        self.frames = []
        self.settings = []
        self.buttons = []
        self.invertedAvailabilityButtons = []
        #self.sample = application.sample
        self.statusText = StringVar()
        self.statusBar = Label(master, textvariable=self.statusText)
        self.timer = Timer()        

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
        val = self.getSettingValue(name)
        return int(val) if val is not None else 0

    def getFloat(self, name):
        val = self.getSettingValue(name)
        return float(val) if val is not None else 0

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

    def clearCanvas(self):
        self.canvas.delete(ALL)
        self.drawAxes()
        self.drawMarks()

    def coordToScreen(self, coord):
        xMargin = self.getInt("xMargin")
        yMargin = self.getInt("yMargin")
        height = self.getInt("height")
        width = self.getInt("width")
        scale = self.getInt("scale")
        return coord[0] * scale + xMargin, coord[1] * scale + yMargin

    def drawAxes(self):
        xMargin = self.getInt("xMargin")
        yMargin = self.getInt("yMargin")
        height = self.getInt("height")
        width = self.getInt("width")
        self.canvas.create_line(xMargin, yMargin, xMargin, height-yMargin)
        self.canvas.create_line(xMargin,yMargin, width-xMargin, yMargin)

    def drawMarks(self):
        xMargin = self.getInt("xMargin")
        yMargin = self.getInt("yMargin")
        height = self.getInt("height")
        width = self.getInt("width")
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
