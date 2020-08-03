import sounddevice as sd
import numpy as np
from gtts import gTTS
import playsound
import random 
import time
import PIL.ImageGrab as IG
import os


def main(duration = 13, threshold = 0.005, cscolor = (7, 35, 52)):
    ''' 
    duration = how long to open the mic for (set it to a little bit higher than your average)
    threshold = mic threshold to detect moves (use testing code below to find what you need)
    cscolor = color of cstimer background when cstimer is running
    '''

    fs = 44100
    while True:
        image = IG.grab()
        color = image.getpixel((10,300))
        print(color)
        time.sleep(1)
        if color == cscolor: # timer running 
            duration = duration # need to solve in 15 seconds
            myrecording = sd.rec(int(duration*fs), samplerate = 44100, channels = 1)

            sd.wait()


            action = myrecording > threshold
            # pause is when action goes from 1 to 0
            pausecounter = 0
            time_paused = 0
            for i in range(len(action)-20000):
                if action[i] == True and action[i+1] == False:
                    if True in action[i+1:i+20000]:
                        pass
                    else:
                        pausecounter+=1
                        # find length of pause
                        pause_start = i+1
                        for j in range(len(action[i+1:-1])):
                            if action[i+1+j] == True:
                                pause_end = i+1+j
                                break
                        
                        time_paused += j
                        print(j)

            time_paused_text = round(time_paused/44100*100)/100

            tts = gTTS('You paused ' + str(pausecounter) + 'times for a total of ' + str(time_paused_text) + 'seconds. ' + pick_insult())
            tts.save('data.mp3')
            playsound.playsound('data.mp3')
            os.remove('data.mp3')



def pick_insult():
    insults = ['You suck.',
        'You ain\'t fast',
        'F you',
        'I like your OLLs. They remind me of my grandpas.',
        'I\'ll feel bad for Erno Rubik if he ever has to see you solve a cube.',
        'It seems like you learn from me',
        'If only you solved as fast as you came.',
        '10 years to be sub 10? Geez man.',
        'Fingertricks Bad.',
        'You think this video will make your YouTube channel more popular. Unfortunately, people just don\'t like you.',
        'cubics? more like noobiks.']

    import random

    insult_num = random.randint(0,len(insults)-1)
    return insults[insult_num]

def testing():
    ''' Use this code to see what levels you need to detect turns'''

    import sounddevice as sd

    fs = 44100
    duration = 10
    myrecording = sd.rec(int(duration*fs), samplerate = 44100, channels = 1)

    sd.wait()

    print(myrecording)

    import matplotlib.pyplot as plt

    plt.plot(myrecording)
    plt.show()

main()