from psychopy import core, visual, event, data
from psychopy.hardware import keyboard
import pandas as pd
import csv
import random
import psychopy.clock
import psychopy.event
import random
import os
import cv2 as cv
from numpy import asarray
import numpy as np
from PIL import Image
import imageio

path = os.getcwd()

win = visual.Window([800,600], fullscr=False, monitor="testMonitor")
myMouse = event.Mouse(visible=True)
finalTable=[['image','Species', 'RespTime','Answer', 'Correct']]

message1= visual.TextStim(win, pos=[0,+0.1],text='Enter the participant number:')
message1.draw()
win.flip()
answer = ''

thisResp=None
while thisResp==None:
    allKeys=event.waitKeys()
    for thisKey in allKeys:  
        if thisKey=='space':
            thisResp=1
        elif thisKey=='return':
            thisResp=1
        elif thisKey=='backspace':
            answer=answer[:-1]
            message1.draw()
            message2 = visual.TextStim(win, pos=[0,-0.1],text=answer)
            message2.draw()
            win.flip()
        else:
            answer += thisKey
            message1.draw()
            message2 = visual.TextStim(win, pos=[0,-0.1],text=answer)
            message2.draw()
            win.flip()

messageVS= visual.TextStim(win, pos=[0,+0.1],text='Visual snow(1) or No visual snow(2)')
messageVS.draw()
win.flip()
visual_answer = ''

thisResp=None
while thisResp==None:
    allKeys=event.waitKeys()
    for thisKey in allKeys:  
        if thisKey=='space':
            thisResp=1
        elif thisKey=='return':
            thisResp=1
        elif thisKey=='backspace':
            answer=answer[:-1]
            messageVS.draw()
            messageVS_2 = visual.TextStim(win, pos=[0,-0.1],text=visual_answer)
            messageVS_2.draw()
            win.flip()
        else:
            visual_answer += thisKey
            messageVS.draw()
            messageVS_2 = visual.TextStim(win, pos=[0,-0.1],text=visual_answer)
            messageVS_2.draw()
            win.flip()

def run(key, thisIncrement):
    # this code gets the landscape as img
    question_link = "/home/bvltesting/Documents/Experiments/Visual_Snow_Experiment/Landscapes"
    
    correct_path = "/home/bvltesting/Documents/Experiments/Visual_Snow_Experiment/Landscapes/Landscape3.jpeg"
    image = imageio.imread(correct_path)/255.0
    img = psychopy.visual.ImageStim(win=win, image=(correct_path),units="pix")

    pause_time = 2    
    img.size = win.size
    
    circle_present = random.choice([True, True, True, True])
    
    # generates noise from negative noise_level to positive noise_level (-1 to 1, in this case)
    # because the shape of the np noise array is (width, height, 1), it can broadcast onto any number of dimensions, meaning you could use grayscale or RGB and still have the 'white static' look.

    rand_radius = random.uniform(0.1, 1)
    right_side = win.size[0]/4
    left_side = 0 - win.size[0]/4
    x = random.choice([left_side, right_side])
    y = 0
    if x == right_side:
        question = 'Right'
    if x == left_side:
        question = 'Left'
    
    right_poly = psychopy.visual.Polygon(win =win, edges= 4, size = (1.5, 3), pos = (0.5,0), ori=45, opacity=0)
    left_poly = psychopy.visual.Polygon(win =win, edges =4, size = (1.5, 3), pos = (-0.5,0), ori =45, opacity =0)

    # Draw the stimulus to the window. We always draw at the back buffer of the window.
    stimClock = core.Clock()

    if key =="1":
        particle_opacity = 1
    elif key =="2":
        particle_opacity =0
    con = 0.05 + thisIncrement
    printed = False
    left_poly.draw()
    right_poly.draw()
    press = False
    if circle_present:
        
        while stimClock.getTime()< 2:
            img.draw()
            circle_stim = psychopy.visual.NoiseStim(win=win, units='pix', size = (256, 256), noiseType ='Uniform', contrast = con,  mask= 'gauss', 
                                                                                    blendmode='add',  noiseFractalPower=-1, color = (1,1, 1), colorSpace  = 'rgb', noiseElementSize=1, ori= 1)
                                                                                    
            circle_stim.pos = (x, y) 
            circle_stim.draw()
            if press == False:
                if myMouse.isPressedIn(right_poly):
                    press = True
                    Resp_Time = stimClock.getTime()
                    if x == right_side:
                        Right = 1
                    if x == left_side:
                        Right = 0
                if myMouse.isPressedIn(left_poly):
                    press = True
                    Resp_Time = stimClock.getTime()
                    if x == right_side:
                        Right = 0
                    if x == left_side:
                        Right = 1
                
            
            win.flip()
           
    else:
        stimClock = core.Clock()
        img.draw()
        win.flip()
        core.wait(2)
    if press == False:
        Resp_Time =0
        Right = 0
    
    row=[question, Resp_Time, Right]
    staircase.addData(Right)
    finalTable.append(row)
    message = visual.TextStim(win, text='+')
    # Draw the stimulus to the window. We always draw at the back buffer of the window.
    message.draw()
    # Flip back buffer and front  buffer of the window.
    win.flip()
    core.wait(0.75)


filename = 'images_'+answer+'.csv'
stepSizeArray =[2]
arrLength = 12
for i in range(arrLength-1):
    stepSizeArray.append(2)

staircase = data.StairHandler(startVal =0.5, stepType ='db',  stepSizes=stepSizeArray, nUp=1, nDown =1, minVal =0, maxVal = 1, nTrials=1)
for i in staircase:
    run(visual_answer, i)
    
print(finalTable)
'''
with open(filename, 'a+', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(finalTable)

'''