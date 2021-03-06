import math
import time
#import PyOpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import numpy as np
from pygame.examples.prevent_display_stretching import user32
from pygame.locals import *
import ctypes
import Shapes
import CameraManagement

# Open Scope for easy access
global perspective
global display
global objArr
global screen
global isRunning
global projection
global camera
global matrix

"""
# CREATE A PYGAME DISPLAY AND OPENGL EVIRONMENT.
#
"""
def createWindow():
    global perspective,screen,display
    pygame.init()
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    display = (screensize[0], screensize[1])
    #SETTING THE DISPLAY UP FOR PYGAME
    screen = pygame.display
    screen.set_mode(screensize, DOUBLEBUF | OPENGL)
    glMatrixMode(GL_PROJECTION)
    perspective = gluPerspective(90, (display[0] / display[1]), 0.3, 555.0)  # fovy, aspect, znear, zfar


"""
#####################################
#
# Function used to find keys pressed
#
#####################################
"""
def getKeys():
    global objArr,isRunning,projection,matrix
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            #matrix = camera.getMatrix()
            #glLoadMatrixf(matrix)

            """
            ###################
            Translating Shapes
            ###################
            """
            if event.key == pygame.K_RIGHT: #Translating shapes
                for obj in objArr:
                    obj.manipulateShape(-1,0,0)
            if event.key == pygame.K_LEFT:
                for obj in objArr:
                    obj.manipulateShape(1, 0, 0)
            if event.key == pygame.K_UP:
                for obj in objArr:
                    obj.manipulateShape(0, 0, 1)
            if event.key == pygame.K_DOWN:
                for obj in objArr:
                    obj.manipulateShape(0, 0, -1)

            if event.key == pygame.K_j: # RESTART GAME FOR NOW
                isRunning=False
                selectObjPopUp()
            if event.key == pygame.K_p: # DEBUGGING
                print(glGetFloatv(GL_PROJECTION_MATRIX))

            if event.key == pygame.K_1: # When key 1 pressed, rotate on Z axis
                try:
                    glPopMatrix()
                except:
                    ""
                try:
                    camera.rotateZ(10)
                    glPushMatrix()
                except:
                    ""
                glMatrixMode(GL_PROJECTION)
            if event.key == pygame.K_2: # When key 2 pressed, rotate on Z axis
                try:
                    glPopMatrix()
                except:
                    ""
                try:
                    camera.rotateZ(-10)
                    glPushMatrix()
                except:
                    ""
                glMatrixMode(GL_PROJECTION)
            projection = glGetFloatv(GL_PROJECTION_MATRIX)
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_position = pygame.mouse.get_pos()

        glMatrixMode(GL_PROJECTION);

"""
############
#
##
###
####
#####
######
####### MAIN RUNNER FUNCTION THAT INITIALIZES SHAPES AND LOOPS UNTIL GAME ENDS....
######
#####
####
###
##
#
############
"""
def main():
    global objArr,isRunning,projection,camera
    createWindow()
    projection = glGetFloatv(GL_PROJECTION_MATRIX)  # MATRICES VALUES....
    camera = CameraManagement.Camera(projection)
    # Creates objects at origin 0,0,0
    cube = Shapes.Cube(5)
    rectangle = Shapes.Rectangle(5, 5, 4,-5,1,-2)
    pyramid = Shapes.Pyramid(-3, -4, 1)
    objArr ={cube,rectangle,pyramid}
    isRunning = True
    while isRunning:
        projection = glGetFloatv(GL_PROJECTION_MATRIX)
        #print (projection)
        glLoadIdentity
        try:
            glLoadMatrixf(camera.getMapped())
        except:
            """"""
        getKeys()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in objArr:
            i.update()
            i.updateColor()
        #UPDATES DIMENSIONS OF EACH OBJECT
        pygame.display.flip()
        pygame.time.wait(50)


"""
#######
#######
##
## As of now, this just resets the game, will implement to display an object pop-up.
##
#######
#######
"""
def selectObjPopUp():
    global screen,display,isRunning
    screen.quit()
    screen.set_mode(display, DOUBLEBUF | OPENGL)
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 200.0)
    glScalef(0.01, 0.01, 0.01)
    gluLookAt(0, 0, 0, 0, 0, -1, 0, 1, 0)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0);
    glVertex3f(0.0, -50.0, -1000.0)
    glTexCoord2f(1.0, 0.0);
    glVertex3f(0.0, -50.0, 100.0)
    glTexCoord2f(1.0, 1.0);
    glVertex3f(100.0, -50.0, 1000.0)
    glTexCoord2f(0.0, 1.0);
    glVertex3f(100.0, -50.0, -1000.0)
    glEnd()
    screen.init()
    main()
    isRunning=True


"""
#
#
# CURRENTLY DOES NOT WORK, SUPPOSED TO ROTATE USER CAMERA BASED ON DRAGGING MOUSE
#
#
"""
def checkClick(obj):
    mpos = pygame.mouse.get_pos()
    z = 2
    ndc = [2.0 * mpos[0] / user32.GetSystemMetrics(0) - 1.0, 1.0 - 2.0 * mpos[1] / user32.GetSystemMetrics(1)]
    tanFov = math.tan(90 * 0.5 * math.pi / 180)
    aspect = user32.GetSystemMetrics(0) / user32.GetSystemMetrics(1)
    viewPos = [z * ndc[0] * aspect * tanFov, z * ndc[1] * tanFov]
    onRect1 = 1 if (
                viewPos[0] >= obj.Vertices[0][0] and viewPos[0] <= obj.Vertices[1][0] and viewPos[1] >= obj.Vertices[0][1] and viewPos[
            1] <= obj.Vertices[2][1]) else 0
    onRect2 = 1 if (
                viewPos[0] >= obj.Vertices[0][0] and viewPos[0] <= obj.Vertices[1][0] and viewPos[1] >= obj.Vertices[0][1] and viewPos[
            1] <= obj.Vertices[2][1]) else 0
    glColor3f(1, 1 - onRect1, 1 - onRect1)
    glBegin(GL_LINES)
    for edge in obj.Edges:
        for vertex in edge:
            glVertex3fv(obj.Vertices[vertex])
    glEnd()
    glColor3f(1, 1 - onRect2, 1 - onRect2)



main()
