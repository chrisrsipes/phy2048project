from __future__ import division
import vis
from visual import *
from visual.controls import *

# globalsasdasda
global state
global horSpring
global verSpring
global attributesLabel

# constants
g = 9.81
deltat = 0.1
mBox = 1
Fgrav = -mBox*g

state = "horizontal"
k = 0.1
t = 0

# customize scenes
scene.width=1024
scene.height=760
scene.x=350
scene.y=0

c = controls(title="Configure Spring Attributes", width=300, height=400)

# visual elements
print(scene.center)
attributesLabel = label(pos=scene.center, color = color.white, height=10, border=6, display=scene)
b = button( pos=(0,60), width=120, height=40, border=0,
              text='Change Spring Orientation', action=lambda: changeOrientation() )
sliderK = slider(pos=(-60,20), width=7, length=120, axis=(1,0), min=0.1, max=10, text="Spring constant", action=lambda: setK(sliderK), color=color.white, value=k)
# sliderKText = text(pos=(0,0), color = color.white, height=10, border=6, display=c)

global sBox
global vBox
global pBox
global springLength
global spring
global ground
global wall

sBox = 0
vBox = 0
pBox = 0
springLength = 0
spring = None
ground = None
wall = None

def resetSprings():
    global sBox
    global vBox
    global pBox
    global springLength
    global spring
    global ground
    global wall
    
    sBox = 0
    vBox = 0
    pBox = 0
    springLength = 0
    spring.visibility = False
    ground.visibility = False
    wall.visibility = False
    del spring
    del ground
    del wall

def showSprings():
    global spring
    global ground
    global wall

    spring.visibility = True
    ground.visibility = True
    wall.visibility = True

#HORIZONTAL SPRING
def HorizontalSpring():
    global k
    global sBox
    global vBox
    global pBox
    global springLength
    global spring
    global ground
    global wall

    resetSprings()
    scene.center = vector(0,0,0)

    #Horizontal Spring Values
    relaxedlength = vector(0.5,0,0)

    #Horizontal Box Object
    sBox = box(pos=(0.05,0,0), size=(0.3,0.3,0.3), color=color.yellow)
    vBox = vector(0,0,0)
    pBox = vector(0,0,0)
    spring = helix(pos=(-0.75,0,0), axis=relaxedlength+sBox.pos+vector(0.1001,0,0),radius=0.1, coils=8, thickness=0.01, color=color.red) 
    springLength = vector(0.05,0,0)

    #Surface Holding Horizontal Spring
    ground = box(size=(1.5,0.02,0.5), pos=(-0.05,-0.16,0))
    wall = box(size=(0.04,0.5,0.3),pos=(-0.77,0.1,0),color=color.white)

    showSprings()



    # done = True
    # while done:
        # rate(100)

        # Fnet = -k*(sBox.pos-springLength)
        # pBox = pBox + Fnet*deltat
        # sBox.pos = sBox.pos + (pBox/mBox)*deltat
        # spring.axis = sBox.pos+relaxedlength+(0.1001,0,0)
 
   
#VERTICAL SPRING
def VerticalSpring():
    global k
    global sBox
    global vBox
    global pBox
    global springLength
    global spring
    global ground
    global wall

    resetSprings()
    scene.center = vector(0,-0.9,0)
    scene.scale = (0.5,0.5,0.5)

    #Vertical Spring Values
    relaxedlength = vector(0,-0.5,0)

    #Vertical Box Object
    sBox = box(pos=(0,0,0), size=(0.3,0.3,0.3), color=color.yellow)
    vBox = vector(0,0,0)
    pBox = vector(0,0,0)
    spring = helix(pos=(0,0.29,0), axis=relaxedlength+sBox.pos+vector(0,0.36,0),radius=0.1, coils=8, thickness=0.01, color=color.red) 
    springLength = vector(0,-0.25,0)
    sBox.pos = springLength + (0,Fgrav/k,0)

    #Surface Holding Vertical Spring
    ground = box(size=(0.75,0.02,0.5), pos=(0,0.3,0))
    wall.visibility = false

    showSprings()

    # done = True
    # while done:
        # rate(100)
 
        # Fnet = -k *(sBox.pos-springLength) + (0, Fgrav, 0)
        # pBox = pBox + Fnet*deltat
        # sBox.pos = sBox.pos + (pBox/mBox)*deltat
        # spring.axis = sBox.pos+relaxedlength+(0,0.36,0)


# will update the visibility of the springs when invoked
# this is based on state
def updateSprings():
  global state

  if state == "horizontal":
    print("h")
    HorizontalSpring()
  else:
    print("v")
    VerticalSpring()

def updateLabel():
  global state
  global attributesLabel
  global k

  tempStr = "orientation: " + state + "\nSpring constant: k=" + str(k)
  attributesLabel.text = tempStr

# change the orientation of the spring
def changeOrientation(): 
  global state
  global attributesLabel

  print(state)

  if state == "horizontal":
    state = "vertical"
  else:
    state = "horizontal"

  attributesLabel.text = "Orientation: " + state
  updateSprings()
  updateLabel()

# change the value of the spring constant k
def setK(sliderK):
  global k
  k = sliderK.value
  updateLabel()
  

# updateSprings()
updateLabel()
scene.select()
