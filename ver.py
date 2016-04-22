from __future__ import division
import vis
from visual import *
from visual.controls import *

### setting up the scene
scene.width = 1024
scene.height = 760
scene.x = 350
scene.center = vector(0,-1.1,0)
scene.scale = (0.4,0.4,0.4)

### constants
deltat = 0.1
g = 9.81
gVector = vector(0, -9.81, 0)
horSceneCenter = (0, 0, 0)
verSceneCenter = (0, -0.9, 0)
verSpringLength = vector(0, 1, 0)
relaxedLength = vector(0, -0.5, 0)
stretchOffset = vector(0, 0.36, 0)

### configurables
k = 12.5
stretch = vector(0, -0.25, 0)
boxMass = 1
horDispConst = vector(0, 0.36, 0)

# global flags
global isRunning
isRunning = False

def calcAxis(relaxedLength, boxPos, stretchOffset):
    return relaxedLength + boxPos + stretchOffset

# class to manage the configurables
class SpringData(object):
    associatedLabel = None
    orientation = ''
    k = 5
    stretch = 0
    Fnet = None
    pBox = None

    def __init__(self, associatedLabel, orientation, k, stretch):
        self.associatedLabel = associatedLabel
        self.orientation = 'Vertical'
        self.k = k
        self.springStretch = stretch

    def generateText(self):
        line1 = 'Orientation : ' + str(self.orientation) + '\n'
        line2 = 'Spring Const: ' + str(self.k) + '\n'
        line3 = 'Stretch: ' + str(self.springStretch) + '\n'
        line4 = 'Momentum: ' + str(self.pBox) + '\n'
        line5 = 'Fnet: ' + str(self.Fnet) + '\n'
        return line1 + line2 + line3 + line4 + line5

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

    def getPBox(self):
        return self.pBox

    def setPBox(self, pBox):
        self.pBox = pBox

    def getFnet(self):
        return self.Fnet

    def setFnet(self, Fnet):
        self.Fnet = Fnet


def setK(sliderK, springData):
    springData.setK(sliderK.value)
    springData.updateAssociatedLabelText()

# setStretch(sliderStretch, springData, spring, sBox, relaxedLength, stretchOffset), color = color.blue, value = stretch[0])
def setStretch(sliderStretch, springData, spring, sBox, relaxedLength, stretchOffset):
    springData.setSpringStretch(vector(0, sliderStretch.value, 0))
    sBox.pos = springData.getSpringStretch() + relaxedLength
    spring.axis = calcAxis(relaxedLength, sBox.pos, stretchOffset)
    springData.updateAssociatedLabelText()

def runDemo(springData, spring, sBox, deltat, boxMass, relaxedLength, calcAxis, gVector):
    global isRunning

    print "in runDemo"
    if (isRunning == False):
        isRunning = True

        count = 0
        pBox = vector(0, 0, 0)
        springData.setPBox(pBox)

        print "set pBox, about to start loop"
        while (count < 100000):
            print count
            rate(25)
            # Fnet = -1 * springData.getK() * (sBox.pos - horSpringLength) + -Fgrav
            tempK = springData.getK()
            tempSprStr = springData.getSpringStretch()
            Fnet = -1 * springData.getK() * springData.getSpringStretch() + (gVector * boxMass)
            pBox = pBox + Fnet * deltat
            sBox.pos = sBox.pos + (pBox / boxMass) * deltat
            springData.setSpringStretch(sBox.pos - relaxedLength)
            spring.axis = calcAxis(relaxedLength, sBox.pos, stretchOffset)
            springData.setPBox(pBox)
            springData.setFnet(Fnet)
            springData.updateAssociatedLabelText()
            count += 1

        isRunning = False

# visual elements
sBox = box(pos = verSpringLength + stretch + (0,-g*boxMass/k,0) , size = (0.3,0.3,0.3), color = color.yellow)
spring = helix(pos = vector(0,0.29,0), axis = calcAxis(relaxedLength, sBox.pos, stretchOffset), radius = 0.1, coils = 8, thickness = 0.01, color = color.red)
ground = box(size=(0.75,0.02,0.5), pos=(0,0.3,0))

attributesLabel = label(pos = scene.center, color = color.white, height = 10, border = 6, display = scene)
springData = SpringData(attributesLabel, 'vertical', k, stretch)
springData.updateAssociatedLabelText()

c = controls(title="Configure Spring Attributes", width=300, height=400)
sliderK = slider(pos = (-50, 0), width=7, length=120, axis=(1,0), min=10, max=15, text="Spring constant", action=lambda: setK(sliderK, springData), color = color.red, value = k)
sliderStretch = slider(pos = (-50, 10), width=7, length=120, axis=(1,0), min=-0.4, max=0.4, text="Spring constant", action=lambda: setStretch(sliderStretch, springData, spring, sBox, relaxedLength, stretchOffset), color = color.blue, value = stretch[0])
buttonRun = button( pos=(0,60), width=120, height=40, border=0,
              text='Run Demo', action=lambda: runDemo(springData, spring, sBox, deltat, boxMass, relaxedLength, calcAxis, gVector) )
