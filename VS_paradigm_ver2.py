from psychopy import core, visual, event
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
myMouse = event.Mouse(visible=False)
finalTable=[['image','Species', 'RespTime','Answer', 'Correct']]

message1= visual.TextStim(win, pos=[0,+0.1],text='Enter the participant number:')
message1.draw()
win.flip()
answer = ''

def run():
    # this code gets the landscape as img
    question_link = "/home/bvlab/Documents/Experiment/Visual_Snow/Landscapes"
    
    path = question_link 
    files=os.listdir(path)
    question=random.choice(files)
    correct_path = path + "//" + question
    # correct_path = "/home/bvlab/Documents/Experiment/Visual_Snow/Stimuli/white.jpg"
    image = Image.open(correct_path)
    img = psychopy.visual.ImageStim(win=win, image=(correct_path),units="pix")

    pause_time = 2    
    img.size = win.size
    
    circle_present = random.choice([True, True, True, True])
    
    #this is for the particle effect
    circle_link = "/home/bvlab/Documents/Experiment/Visual_Snow/Stimuli/circle.png"
    pink_link = "/home/bvlab/Documents/Experiment/Visual_Snow/Stimuli/yellow.jpg"
    # img = Image.open(circle_link)
    circle = imageio.imread(circle_link)/255.0
    
    # generates noise from negative noise_level to positive noise_level (-1 to 1, in this case)
    # because the shape of the np noise array is (width, height, 1), it can broadcast onto any number of dimensions, meaning you could use grayscale or RGB and still have the 'white static' look.

    rand_radius = random.uniform(0.1, 1)
    x = random.uniform(-1,1)
    y = random.uniform(-1,1)
    
    # Draw the stimulus to the window. We always draw at the back buffer of the window.
    stimClock = core.Clock()
    noise_level = random.choice([0.1, 1, 10, 100, 1000])
    # noise_level = random.uniform(0.1, 10000)
    noise_level = 10000000000
    if circle_present:
       
        while stimClock.getTime()< 2:
            
            img.draw()
            # Pause 2 s, so you get a chance to see it!
        
            noise = random.uniform(5, 10)
            
            presented = circle + 2*np.random.random((circle.shape[0],circle.shape[1], 1))*noise_level-noise_level 
            presented = Image.fromarray((presented * 100).astype(np.uint8))
            
            circle_stim = psychopy.visual.ImageStim(win=win, image=presented, opacity = 1, mask='gauss')
            
            # circle_stim = psychopy.visual.NoiseStim(win=win, noiseImage = circle_link, size = rand_radius, noiseType ='White', blendmode='add',  color = (-1,-1, -1), colorSpace  = 'rgb',
            #                                                                       mask = 'gauss', ori=1, texRes=52) #, filter='None')
            circle_stim.pos = (x, y) 
            circle_stim.size = rand_radius
            circle_stim.draw()
            win.flip()
            # core.wait(2)
  
    else:
        stimClock = core.Clock()
        img.draw()
        win.flip()
        core.wait(2)
    
    key = psychopy.event.getKeys(keyList =['b'], timeStamped = stimClock)
    
    if len(key)>0:
        ans='1'
        find = key[0]
        Resp_Time=find[1]
        if circle_present:
            Right = "Correct"
        else:
            Right = "Incorrect"
            
    else:
        ans = '0'
        Resp_Time = 0
        Answer ='0'
        if not circle_present:
            Right = "Correct"
        else:
            Right = "Incorrect"
            
    row=[question, Resp_Time, ans, Right]
    finalTable.append(row)
    message = visual.TextStim(win, text='+')
    # Draw the stimulus to the window. We always draw at the back buffer of the window.
    message.draw()
    # Flip back buffer and front  buffer of the window.
    win.flip()
    core.wait(0.75)

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




filename = 'images_'+answer+'.csv'
for i in range(8):
    run()
'''
with open(filename, 'a+', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(finalTable)

'''