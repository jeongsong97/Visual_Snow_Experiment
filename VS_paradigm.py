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

path = os.getcwd()

win = visual.Window([800,600], fullscr=False, monitor="testMonitor")
myMouse = event.Mouse(visible=False)
finalTable=[['image','Species', 'RespTime','Answer', 'Correct']]

message1= visual.TextStim(win, pos=[0,+0.1],text='Enter the participant number:')
message1.draw()
win.flip()
answer = ''

def processor(image):
  row,col= image.shape
  mean = 0
  var = random.uniform(0.05, 0.30)
  sigma = var**0.5
  gauss = np.random.normal(mean,sigma,(row,col))
  gauss = gauss.reshape(row,col)
  noisy = image + gauss
  return noisy


def run():
    # this code gets the landscape as img
    question_link = "/home/bvlab/Documents/Experiment/Visual_Snow/Landscapes"
    path = question_link 
    files=os.listdir(path)
    question=random.choice(files)
    correct_path = path + "//" + question
    image = Image.open(correct_path)
    img = psychopy.visual.ImageStim(win=win, image=(correct_path),units="pix")

    pause_time = 2    
    img.size = win.size
    
    #this is for the particle effect
    rand_radius = random.uniform(0.01, 0.30)
    circle = psychopy.visual.Circle(win=win,  radius =rand_radius, fillColor=(128, 255, 128), opacity =0.4, colorSpace='rgb')
    x = random.uniform(-1,1)
    y = random.uniform(-1,1)
    circle.pos = (x, y) 
    # Draw the stimulus to the window. We always draw at the back buffer of the window.
    img.draw()
    circle.draw()
    
    # Flip back buffer and front  buffer of the window.
    win.flip()
    data = asarray(image)
    image1LAB = cv.cvtColor(data, cv.COLOR_BGR2LAB)
    
    L1, a1, b1 = cv.split(asarray(win._getFrame()))
    
    L1_MeanValue = np.mean(L1.flat)
    L1_WithZeroMean = L1 - L1_MeanValue
    L1_StDev = np.std(L1_WithZeroMean.flat)
    L1_Normalised = L1_WithZeroMean / L1_StDev
    
    L1_NormalisedProcessed = processor(L1_Normalised)

    L1_Processed = L1_NormalisedProcessed * L1_StDev + L1_MeanValue
    print(L1_Processed)
    print(L1_Processed.shape)
    image1Processed = Image.fromarray(L1_Processed)
    # image1Processed = cv.cvtColor([L1_Processed, a1, b1], cv.COLOR_LAB2BGR)
    pix_img = psychopy.visual.ImageStim(win=win, image=image1Processed, units="pix")
    pix_img.draw()
    win.flip()
    
    # Pause 2 s, so you get a chance to see it!
    core.wait(pause_time)
        
    stimClock = core.Clock()
    key = psychopy.event.getKeys(keyList =['0','1'], timeStamped = stimClock)
    if len(key)>0:
        ans=key[len(key) -1]
        Resp_Time=ans[1]
    else:
        ans = '0'
        Resp_Time = 0
    '''
    if len(key)>0:
        ans=key[len(key) -1]

        Resp_Time=ans[1]
        x = ans[0]
        if x=='2':
            Answer="1"
            if random_list [i] == 1:
                Right = "Correct"
            if random_list [i] == 0:
                Right = "Incorrect"
    else:
        Answer = '0'
        Resp_Time = 0
        if random_list [i] == 1:
            Right = "Incorrect"
        if random_list [i] == 0:
            Right = "Correct"
    '''
    row=[question, Resp_Time, ans]
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
for i in range(4):
    run()
'''
with open(filename, 'a+', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(finalTable)

'''