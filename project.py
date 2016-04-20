from __future__ import division
import vis
from visual import *
from visual.controls import *

scene.width = 1024
scene.height = 760
scene.x = 350
scene.y = 0

# constants


# spring visual elements
spring = None
wall = None
ground = None

# boxPosition, boxVelocity, boxMass
# springPosition, springAxis, springLength

def loadHorizontal(spring, wall, ground, boxPosition, boxVelocity, boxMass, springPosition, springAxis, springLength):
    sBox = box(pos = boxPosition, size = (0.3, 0.3, 0.3), color = color.yellow)
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
    ground = box(size = (0.04, 0.5, 0.3), pos = (-0.77, 0.1, 0), color = color.white)
    wall = box(size = (0.04, 0.5, 0.3), pos = (-0.77, 0.1, 0), color = color.white)
        

def initHorizontal(spring, ground, wall):
    relaxedLength = (0.5, 0, 0)
    
    initBoxPosition = (-0.05, -0.16, 0)
    initBoxVelocity = (0, 0, 0)
    initBoxMass = 1
    
    initSpringPosition = (-0.75, 0, 0)
    initSpringAxis = relaxedLength + initBoxPosition + (0,1001, 0, 0)
    initSpringLength = (0.05, 0, 0)
    
    loadHorizontal(spring, wall, ground, initBoxPosition, initBoxVelocity, initBoxMass, 
                    initSpringPosition, initSpringAxis, initSpringLength)

initHorizontal(spring, ground, wall)

# sBox = box(pos = initBoxPosition, axis = boxAxis, radius = boxRadius, coils = coilCount, color = springColor)
# vBox = initVelocity
# pBox = boxMass * vBox
    



