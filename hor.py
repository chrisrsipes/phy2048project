from __future__ import division
import vis
from visual import *
from visual.controls import *

### setting up the scene
scene.width = 1024
scene.height = 760
scene.x = 350

### constants
deltat = 0.1
g = 9.81
horSceneCenter = (0, 0, 0)
verSceneCenter = (0, -0.9, 0)
horSpringLength = vector(1, 0, 0)
relaxedLength = vector(0.5, 0, 0)
stretchOffset = vector(0.1001, 0, 0)

### configurables
k = 0.1
stretch = vector(0.05, 0, 0)
boxMass = 1
horDispConst = vector(0.1001, 0, 0)

# global flags
global isRunning
isRunning = False

def calcAxis(relaxedLength, boxPos, stretchOffset):
    return relaxedLength + boxPos + stretchOffset

# class to manage the configurables
class SpringData(object):
    associatedLabel = None
    orientation = ''
    k = 0.1
    stretch = 0

    def __init__(self, associatedLabel, orientation, k, stretch):
        self.associatedLabel = associatedLabel
        self.orientation = 'horizontal'
        self.k = k
        self.springStretch = stretch

    def generateText(self):
        line1 = 'Orientation : ' + str(self.orientation) + '\n'
        line2 = 'Spring Const: ' + str(self.k) + '\n'
        line3 = 'Stretch: ' + str(self.springStretch) + '\n'
        return line1 + line2 + line3

    def updateAssociatedLabelText(self):
        if (self.associatedLabel != None):
            self.associatedLabel.text = self.generateText()
        else:
            print("Error: associated label was not defined.")

    def getOrientation(self):
        return self.orientation

    def setOrientation(self, orientation):
        self.orientation = orientation

    def getK(self):
        return self.k

    def setK(self, k):
        self.k = k

    def getSpringStretch(self):
        return self.springStretch

    def setSpringStretch(self, stretch):
        self.springStretch = stretch

    def getSpring(self):
        return self.spring

    def setSpring(self, spring):
        self.spring = spring

def setK(sliderK, springData):
    springData.setK(sliderK.value)
    springData.updateAssociatedLabelText()

def setStretch(sliderStretch, springData):
    springData.setSpringStretch(sliderStretch.value)
    springData.updateAssociatedLabelText()

def runDemo(springData, spring, sBox, deltat, boxMass, relaxedLength, calcAxis):
    global isRunning
    if (isRunning == False):
        isRunning = True

        count = 0
        pBox = vector(0, 0, 0)
        while (count < 1000):
            rate(100)
            print count
            print 'springStretch'
            print springData.getSpringStretch()
            # Fnet = -1 * springData.getK() * (sBox.pos - horSpringLength)
            Fnet = -1 * springData.getK() * springData.getSpringStretch()
            print 'fnet is okay'
            pBox = pBox + Fnet * deltat
            print 'pbox is okay'
            sBox.pos = sBox.pos + (pBox / boxMass) * deltat
            print 'sBox.pos is okay'
            springData.setSpringStretch(sBox.pos - relaxedLength)
            print 'setting spring stretch is okay'
            spring.axis = calcAxis(relaxedLength, sBox.pos, stretchOffset)
            print 'spring axis is okay'
            count += 1

        isRunning = False

# visual elements
sBox = box(pos = horSpringLength + stretch, size = (0.3,0.3,0.3), color = color.yellow)
spring = helix(pos = vector(-0.75,0,0), axis = calcAxis(relaxedLength, sBox.pos, stretchOffset), radius = 0.1, coils = 8, thickness = 0.01, color = color.red)
ground = box(size=(1.5,0.02,0.5), pos=(-0.05,-0.16,0))
wall = box(size=(0.04,0.5,0.3),pos=(-0.77,0.1,0),color=color.white)

attributesLabel = label(pos = scene.center, color = color.white, height = 10, border = 6, display = scene)
springData = SpringData(attributesLabel, 'horizontal', k, stretch)
springData.updateAssociatedLabelText()

c = controls(title="Configure Spring Attributes", width=300, height=400)
sliderK = slider(pos = (-50, 0), width=7, length=120, axis=(1,0), min=0.1, max=10, text="Spring constant", action=lambda: setK(sliderK, springData), color = color.red, value = k)
sliderStretch = slider(pos = (-50, 10), width=7, length=120, axis=(1,0), min=0.1, max=10, text="Spring constant", action=lambda: setStretch(sliderStretch, springData), color = color.blue, value = stretch[0])
buttonRun = button( pos=(0,60), width=120, height=40, border=0,
              text='Run Demo', action=lambda: runDemo(springData, spring, sBox, deltat, boxMass, relaxedLength, calcAxis) )
