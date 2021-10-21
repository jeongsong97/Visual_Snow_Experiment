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

def run(key, i):
    # this code gets the landscape as img
    question_link = "/home/bvlab/Documents/Experiment/Visual_Snow/Landscapes"
    
    path = question_link 
    files=os.listdir(path)
    question=random.choice(files)
    correct_path = path + "//" + question
    correct_path = "/home/bvlab/Documents/Experiment/Visual_Snow/Landscapes/Landscape3.jpeg"
    image = imageio.imread(correct_path)/255.0
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
    right_side = win.size[0]/4
    left_side = 0 - win.size[0]/4
    x = random.choice([left_side, right_side])
    y = 0
    
    # Draw the stimulus to the window. We always draw at the back buffer of the window.
    stimClock = core.Clock()
    # noise_level = random.choice([0.1])
    # noise_level = random.uniform(0.1, 10000)
    noise_level = 0.2 #  0.00001
    circle_noise_level = 0 # 1000
    noises = [0.2, 0.5, 0.7, 1, 1.2, 1.5, 1.7, 2]
    stim_opa = [0.1, 0.15, 0.2, 0.6, 0.5, 0.7, 0.8, 1]
    if key =="1":
        particle_opacity = 1
    elif key =="2":
        particle_opacity =0
    printed = False
    if circle_present:
        circle_noise_level = noises[i]
        opa = stim_opa[i]
        while stimClock.getTime()< 2:
            # noise = random.uniform(0,  0.0001)
            # if i == 0:
                # print(back_image)
            img.draw()

            circle_stim = psychopy.visual.NoiseStim(win=win, noiseImage = circle_link, mask= 'gauss', size = (250, 250), units='pix', opacity = opa, noiseType ='Normal', 
                                                                                    blendmode='add', color = (1,1, 1), colorSpace  = 'rgb', noiseElementSize=circle_noise_level, ori= 1)
            circle_stim.pos = (x, y) 
            circle_stim.draw()
            
            background = psychopy.visual.NoiseStim(win=win, noiseImage = circle_link, units='pix', size = win.size, noiseType ='Uniform', opacity =particle_opacity, 
                                                                                        blendmode='add',  noiseFractalPower=-1, color = (1,1, 1), colorSpace  = 'rgb', noiseElementSize=1,
                                                                                    ori= 1) #, filter='None')
            background.draw()
            
            
            '''
            if i ==6:
                if printed == False:
                    with open('/home/bvlab/Documents/Experiment/Visual_Snow/test1.txt', 'w') as outfile:
                        for slice_2d in presented:
                            np.savetxt(outfile, slice_2d)
                    printed =True
            '''
           
            win.flip()
            
            # Pause 2 s, so you get a chance to see it!
            core.wait(0.1)
    
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





filename = 'images_'+answer+'.csv'
for i in range(8):
    run(visual_answer, i)
'''
with open(filename, 'a+', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(finalTable)

'''