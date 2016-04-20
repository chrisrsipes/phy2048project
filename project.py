from __future__ import division
import vis
from visual import *
from visual.controls import *

### setting up the scene
scene.width = 1024
scene.height = 760
scene.x = 350
scene.y = 0

### constants
deltat = 0.1
g = 9.81
horSceneCenter = (0, 0, 0)
verSceneCenter = (0, -0.9, 0)

### configurables

# for immutable types in python, we have to get a little
# hacky to make this able to be changed during runtime.
# We must wrap it in an object, for example a list
orientationWrapper = ['horizontal']
kWrapper  = [0.1]
boxMass = 1
horDispConst = vector(0.1001, 0, 0)
horSpringLength = (0.05, 0, 0)
verSpringLength = (0, -0.25, 0)

### constant forces
Fgrav = -1 * boxMass * g

### Utility Classes
class LabelText(object):
    orientation = ""
    k = 0.1
    associatedLabel = None

    def __init__(self, associatedLabel, orientation, k):
        self.associatedLabel = associatedLabel
        self.orientation = orientation
        self.k = k

    def generateText(self):
        return 'Orientation: ' + self.orientation + '\n'

    def updateAssociatedLabelText(self):
        self.associatedLabel.text = self.generateText()

    def getOrientation(self):
        return self.orientation

    def setOrientation(self, newOrientation):
        self.orientation = newOrientation

### spring visual elements
spring = None
wall = None
ground = None

### functions

# loads the horizontal objects into spring, wall, and ground
# will set and return boxPosition, boxVelocity, and boxMass
def loadHorizontal(spring, wall, ground, boxPosition, boxVelocity, boxMass, springPosition, springAxis, springLength):
    sBox = box(pos = boxPosition, size = vector(0.3, 0.3, 0.3), color = color.yellow)
    vBox = boxVelocity
    pBox = boxMass * boxVelocity

    if (spring != None):
        spring.visible = false
        spring = None

    if (ground != None):
        ground.visible = false
        ground = None

    if (wall != None):
        wall.visible = None
        wall = None

    spring = helix(pos = springPosition, axis = springAxis, radius = 0.1, coils = 8, thickness = 0.1, color = color.red)
    ground = box(size = vector(0.04, 0.5, 0.3), pos = vector(-0.77, 0.1, 0), color = color.white)
    wall = box(size = vector(0.04, 0.5, 0.3), pos = vector(-0.77, 0.1, 0), color = color.white)

    return (spring, wall, ground, sBox, vBox, pBox)

# loads the vertical objects into spring, wall, and ground
# will set and return boxPosition, boxVelocity, and boxMass
def loadVertical(spring, wall, ground, boxPosition, boxVelocity, boxMass, springPosition, springAxis, springLength):
    sBox = box(pos = boxPosition, size = vector(0.3, 0.3, 0.3), color = color.yellow)
    vBox = boxVelocity
    pBox = boxMass * boxVelocity

    if (spring != None):
        spring.visible = false
        spring = None

    if (ground != None):
        ground.visible = false
        ground = None

    if (wall != None):
        wall.visible = None
        wall = None

    spring = helix(pos = springPosition, axis = springAxis, radius = 0.1, coils = 8, thickness = 0.1, color = color.red)
    ground = box(size = vector(0.75, 0.02, 0.5), pos = vector(0, -.25, 0), color = color.white)
    # no wall

    return (spring, wall, ground, sBox, vBox, pBox)


# initializes a horizontal comopenent
def initHorizontal(spring, wall, ground, horSpringLength, boxMass, scene, sceneCenter):
    scene.center = sceneCenter

    relaxedLength = vector(0.5, 0, 0)

    initBoxPosition = vector(-0.05, -0.16, 0)
    initBoxVelocity = vector(3, 0, 0)

    initSpringPosition = vector(-0.75, 0, 0)
    initSpringAxis = relaxedLength + initBoxPosition + vector(0.1001, 0, 0)

    return loadHorizontal(spring, wall, ground, initBoxPosition, initBoxVelocity, boxMass, initSpringPosition, initSpringAxis, horSpringLength)
    # return (spring, ground, wall) + loadHorizontal(spring, wall, ground, initBoxPosition, initBoxVelocity, boxMass, initSpringPosition, initSpringAxis, horSpringLength)

# initializes a vertical comopenent
def initVertical(spring, wall, ground, horSpringLength, boxMass, scene, sceneCenter):
    scene.center = sceneCenter

    relaxedLength = vector(0, -0.5, 0)

    initBoxPosition = vector(0, 0, 0)
    initBoxVelocity = vector(0, 0, 0)

    initSpringPosition = vector(0, 0.29, 0)
    initSpringAxis = relaxedLength + initBoxPosition + vector(0, 0.36, 0)

    return loadVertical(spring, wall, ground, initBoxPosition, initBoxVelocity, boxMass, initSpringPosition, initSpringAxis, horSpringLength)

def runDemo(orientationWrapper, loadVertical, loadHorizontal, spring, wall, ground, initBoxPosition, initBoxVelocity, boxMass, initSpringAxis, horSpringLength):
    if (orientationWrapper[0] == 'horizontal'):
        loadHorizontal(spring, wall, ground, initBoxPosition, initBoxVelocity, boxMass, initSpringPosition, initSpringAxis, horSpringLength)
    else:
        loadVertical(spring, wall, ground, initBoxPosition, initBoxVelocity, boxMass, initSpringPosition, initSpringAxis, horSpringLength)


### start horizontal
(spring, wall, ground, sBox, vBox, pBox) = initVertical(spring, wall, wall, horSpringLength, boxMass, scene, verSceneCenter)


### general visual elements
attributesLabel = label(pos = scene.center, color = color.white, height = 10, border = 6, display = scene)
attributesLabelText = LabelText(attributesLabel, orientationWrapper[0], kWrapper[0])
attributesLabelText.updateAssociatedLabelText()

### sets up the control window

c = controls(title="Configure Spring Attributes", width=300, height=400)

def changeOrientation(orientationWrapper, attributesLabelText):
    if (orientationWrapper[0] == 'horizontal'):
        orientationWrapper[0] = 'vertical'
    else:
        orientationWrapper[0] = 'horizontal'

    attributesLabelText.setOrientation(orientationWrapper[0])
    attributesLabelText.updateAssociatedLabelText()

btnOrientation = button(pos = (0, 60), width = 120, height = 40, border = 0, text = 'Change String Orientation', action = lambda: changeOrientation(orientationWrapper, attributesLabelText))



#  count = 0
# while (count < 100):
#     count += 1
#     Fnet = -k * (sBox.pos - horSpringLength)
#     pBox = pBox + Fnet * deltat
#     sBox.pos = sBox.pos + (pBox / boxMass) * deltat
#     spring.axis = sBox.pos + horSpringLength + horDispConst

# sBox = box(pos = initBoxPosition, axis = boxAxis, radius = boxRadius, coils = coilCount, color = springColor)
# vBox = initVelocity
# pBox = boxMass * vBox
