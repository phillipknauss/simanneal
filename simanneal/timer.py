import time

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
        self.runTime = time.clock() - self.lastStart

    def report(self):
        if self.lastStart is None:
            return
        if self.runTime is None:
            runTime = time.clock() - self.lastStart
        else:
            runTime = self.runTime
        print("Run duration: ", runTime)
