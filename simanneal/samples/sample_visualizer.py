""" Sample of simulated annealing using simanneal and visualizer modules """

import threading
import time
import pickle
import json
import random
import math
from tkinter import *

from twodimensional import TwoDimensionalSample
from simanneal.timer import Timer
from simanneal.visualizer import GUI

global window  

class Application(object):
    def __init__(self):
        self.sample = TwoDimensionalSample()
        self.sample.reportFunction = self.updateProgress

        self.buildUI(self.sample)
        self.window.clearCanvas()
        self.genRandom(100)

        self.window.master.mainloop()

    def buildUI(self, sample):
    
        self.window = GUI()
            
        self.window.addSetting("xMargin","10")
        self.window.addSetting("yMargin","10")
        self.window.addSetting("width","200")
        self.window.addSetting("height","200")
        self.window.addSetting("scale","1")

        self.window.addSetting("maxCount","1000000")
        self.window.addSetting("minEnergy","850")
        self.window.addSetting("reportPeriod","1000")
        self.window.addSetting("alpha","1")
    
        f0 = self.window.addFrame("data_import_export", Frame(self.window.master))
        self.window.addButton("import", Button(f0, text="Import Data", command=lambda : self.window.run_threaded(self.import_data)))
        self.window.addButton("export", Button(f0, text="Export Data", command=lambda : self.window.run_threaded(self.export_data)))
        f1 = self.window.addFrame("json_import_export", Frame(self.window.master))
        self.window.addButton("import_json", Button(f1, text="Import JSON", command=lambda : self.window.run_threaded(self.import_json)))
        self.window.addButton("export_json", Button(f1, text="Export JSON", command=lambda : self.window.run_threaded(self.export_json)))
        f2 = self.window.addFrame("generators", Frame(self.window.master))
        self.window.addButton("parabolic", Button(f2, text="Parabolic", command=lambda : self.window.run_threaded(self.parabolic)))
        self.window.addButton("cubic", Button(f2, text="Cubic", command=lambda : self.window.run_threaded(self.cubic)))
        self.window.addButton("random", Button(f2, text="Random", command=lambda : self.window.run_threaded(self.randomize)))
        f3 = self.window.addFrame("actions", Frame(self.window.master))
        self.window.addButton("anneal", Button(f3, text="Anneal", command=lambda : self.window.run_threaded(self.anneal)))
        self.window.addButton("improve", Button(f3, text="Improve", command=lambda : self.window.run_threaded(self.improve)))
        stopButton = Button(f3, text="Stop", command=self.stop, state=DISABLED)
        self.window.addButton("stop", stopButton)
        self.window.invertedAvailabilityButtons.append(stopButton)

        self.window.build()

    def updateUIFromSample(self):
        self.window.update(self.sample.state, self.sample.E(self.sample.state))

    def stop(self):
        # This sometimes crashes the python runtime... needs to be fixed
        self.sample.stop()
        self.updateUIFromSample()
        
    def anneal(self):
        print("anneal")
        self.window.statusText.set("Annealing...")

        self.sample.maxCount = self.window.getInt("maxCount")
        self.sample.minEnergy = self.window.getInt("minEnergy")
        self.sample.reportPeriod = self.window.getInt("reportPeriod")
        self.sample.alpha = self.window.getFloat("alpha")
    
        optimized = self.sample.run()
        self.sample.state = optimized["bestState"] # Prime annealer for reuse
        self.window.update(optimized["bestState"], optimized["bestEnergy"])

    def updateProgress(self, status):
        elapsed = time.clock()
        self.window.statusText.set("Elapsed: {0:.2f}".format(elapsed-self.window.timer.lastStart) + "(" + "{0:.2f}".format(status["bestEnergy"]) + ")")
        
        if self.sample.state != status["bestState"] and type(status["bestState"]) is list:
            self.sample.state = status["bestState"]
            self.window.clearCanvas()
            self.window.drawCoords(status["bestState"])

    def improve(self):
        "Update initialState with candidates until energy improves once"

        print("improve")
        self.window.statusText.set("Improving...")
        startEnergy = self.sample.E(self.sample.state)
        energy = startEnergy
        print(self.sample.annealer.stop)
        while energy >= startEnergy and self.sample.annealer.stop is not True:
            self.sample.state = self.sample.neighbor(self.sample.state)
            energy = self.sample.E(self.sample.state)
            
        self.updateUIFromSample()

    def parabolic(self):
        coords = []
        for i in range(-20,20):
            coords.append( (i+100, ((i)*(i))/10+100) )
        self.sample.state = coords
        self.updateUIFromSample()

    def cubic(self):
        coords = []
        for i in range(-20,20):
            coords.append( (i+100, ((i)*(i)*(i))/100+100) )
        self.sample.state = coords
        self.updateUIFromSample()

    def randomize(self):
        "Update State to a random order"

        print("randomize")
        for n in self.sample.state:
            self.sample.state = self.sample.neighbor(self.sample.state)
        self.updateUIFromSample()  

    def import_data(self):
        print("import")
        with open('data.dat', mode='rb') as file:
            self.sample.state = pickle.load(file)
        self.updateUIFromSample()

    def export_data(self):
        print("export")
        with open('data.dat', mode='wb') as file:
            pickle.dump(self.sample.state, file)
        self.updateUIFromSample()

    def export_json(self):
        print("export_json")
        with open('data.json', mode='w') as file:
            json.dump(self.sample.state, file)
        self.updateUIFromSample()

    def import_json(self):
        with open('data.json', mode='r') as file:
            self.sample.state = json.load(file)
        self.updateUIFromSample()

    def export_bitmap(self):
        print("export_bitmap - not implemented")

    def import_bitmap(self):
        print("import_bitmap - not implemented")   
   
    def genRandom(self, count):
        initialState = []
        for i in range(0,100):
            x, y = random.randint(0,180), random.randint(0,180)
            initialState.append( (x,y) )

        self.sample.state = initialState
        self.updateUIFromSample()

if __name__ == '__main__': application = Application()
