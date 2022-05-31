"""
Noise Masking Experiment
Authors: Jeong Ung Song, Annabel Wing-Yan Fan & Alexander Baldwin, Baldwin Vision Lab 2021/2022
Version: af_0.1

Description:
A noisy stimulus grating is shown on top of a landscape picture.

The participant responds by touching the location of the stimulus grating.
The contrast of the grating is adjusted using a staircase, within each block the level of noise is kept constant. 

The goal is to use the noise masking paradigm to determine the participant's level of internal (equivalent) noise.

Outputs: 
- stimulus parameters (phase, spatial frequency, etc.)
- experiment parameters
"""
from psychopy import core, visual, event, data, gui
from psychopy.preferences import prefs
from psychopy.hardware import keyboard
import pandas as pd
import csv
import random
import os
from numpy import asarray
import numpy as np
import imageio

# Store info about the experiment session
psychopyVersion = '2021.2.3'
expName = ' Visual Snow Experiment' 
expInfo = {'participant': '', 'session': '001', 'startContrast': 0.6, 'condition':['Test', 'Control'], 'debug':['True','False']}

dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Start-Up Message

path = os.getcwd()

win = visual.Window([1920,1080], fullscr=True, monitor="testMonitor")
prefs.general['shutdownKey'] = 'q'
event.globalKeys.add(key='q', func=core.quit, name='shutdown')

def run(thisIncrement, count):
    # this code gets the landscape as img
    question_link = "/home/bvltesting/Documents/Experiments/Visual_Snow_Experiment/Landscapes"
    correct_path = "/home/bvltesting/Documents/Experiments/Visual_Snow_Experiment/Landscapes/Landscape3.jpeg"
    image = imageio.imread(correct_path)/255.0
    img = visual.ImageStim(win=win, image=(correct_path),units="pix")

    pause_time = 2    
    img.size = win.size
    
    # generates noise from negative noise_level to positive noise_level (-1 to 1, in this case)
    # because the shape of the np noise array is (width, height, 1), it can broadcast onto any number of dimensions, meaning you could use grayscale or RGB and still have the 'white static' look.

    right_side = win.size[0]/4
    left_side = 0 - win.size[0]/4
    x = random.choice([left_side, right_side])
    y = 0
    if x == right_side:
        question = 'Right'
    if x == left_side:
        question = 'Left'
    
    # Create two regions for the participant to click.
    right_poly = visual.Polygon(win =win, edges= 4, size = (1.45, 3), pos = (0.5,0), ori=45, opacity=1)
    left_poly = visual.Polygon(win =win, edges =4, size = (1.45, 3), pos = (-0.5,0), ori =45, opacity =1)

    # Draw the stimulus to the window. We always draw at the back buffer of the window.
    stimClock = core.Clock()
    con = 0.05 + thisIncrement
    printed = False
    left_poly.draw()
    right_poly.draw()
    pressed = False
    myMouse = event.myMouse = event.Mouse(visible=True, newPos = [0,0])

    while stimClock.getTime()< 2.5:
        img.draw()
        circle_stim = visual.NoiseStim(win=win,  units='pix', 
                                size = (512, 512), noiseType ='Uniform', contrast = con,  
                                mask= 'gauss', blendmode='add',  noiseFractalPower=-1, 
                                color = (1,1, 1), colorSpace  = 'rgb', noiseElementSize=1, ori= 1)
        circle_stim.pos = (x, y) 
        circle_stim.draw()
        
        if pressed == False:
            a = myMouse.getPos()
            if a[0] > 0.1:
                answer = 'right'
                pressed = True
                Resp_Time = stimClock.getTime()
                if x == right_side:
                    Right = 1
                if x == left_side:
                    Right = 0
            elif a[0] < -0.1:
                answer = 'left'
                pressed = True
                Resp_Time = stimClock.getTime()
                if x == right_side:
                    Right = 0
                if x == left_side:
                    Right = 1
        win.flip()
    if pressed == False:
        answer = 'None'
        Resp_Time =0
        Right = 0
    
    message = visual.TextStim(win, text='+')
    # Draw the stimulus to the window. We always draw at the back buffer of the window.
    message.draw()
    # Flip back buffer and front  buffer of the window.
    win.flip()
    core.wait(0.75)


stepSizeArray =[2]
arrLength = 5
trials =[0.9, 0.8, 0.7]
count =0
for i in trials:
    run(i, count)
    count = count +1
    
