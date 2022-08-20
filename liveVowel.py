#!/usr/bin/env python3 

import matplotlib.pyplot as plt
import numpy as np
import math
import parselmouth
from parselmouth import praat
import pyaudio
from ctypes import *

# Constants for sampling
nSamples = 4096       # number of samples 
nSamples = 8192 # number of samples 
samplingRate = 44100  # sampling rate in Hz
samplingRate *= 4  # sampling rate in Hz
nSamples *= 4

pausa = nSamples/samplingRate*200
print(pausa)

#####################
# Setup the stage

fig = plt.figure()
plt.xlim(-2500, -500)
plt.ylim(-900,-200)

def addReferencePoint(label, f1, f2, f3) :
  plt.annotate(label,
               (-f2,-f1),
               textcoords="offset points",
               xytext=(0,5), # text to point distance 
               ha='center') # align 
  plt.plot(-f2,-f1,marker='o',color='k')

# Reference points are drawn here
addReferencePoint("i", 288.7, 2371.8, 3258)
addReferencePoint("y", 285.8, 2176.8, 2393.9)
addReferencePoint("u", 300.6, 751.7, 2347.5)
addReferencePoint("e", 439.1, 2181.4, 2793.8)
addReferencePoint("ø", 448.3, 1641.3, 2025.1)
addReferencePoint("ɘ", 416.9, 1942, 2362.6)
addReferencePoint("o", 416.3, 751.5, 2121.8)
addReferencePoint("ɔ", 585.1, 890.3, 2241.8)
addReferencePoint("ε", 613.8, 1897.1, 2533.1)
addReferencePoint("ɶ", 560.1, 1488.4, 1914.9)
addReferencePoint("aᶠ", 834.3, 1422.9, 1851.5)
addReferencePoint("aᶜ", 739, 1200.4, 2166.6)
addReferencePoint("ɑ", 770.8, 1081.6, 2186.1)

####################################
# define functions to analyze data

def Average(arr) :
    l = len(arr)
    if l==0 : return 0
    return sum(arr)/len(arr)

def analyzeSound(myData, sampling):
    # Vector constructor listed here
    # https://parselmouth.readthedocs.io/en/stable/api_reference.html#parselmouth.Sound.__init__
    sound = parselmouth.Sound(myData, sampling_frequency=sampling)
    f0min=75
    f0max=300
    pointProcess = praat.call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    formants = praat.call(sound, "To Formant (burg)", 0.0025, 5, 5000, 0.025, 50)
    numPoints = praat.call(pointProcess, "Get number of points")
    f1_list = []
    f2_list = []
    f3_list = []
    for point in range(0, numPoints):
        point += 1
        t = praat.call(pointProcess, "Get time from index", point)
        f1 = praat.call(formants, "Get value at time", 1, t, 'Hertz', 'Linear')
        f2 = praat.call(formants, "Get value at time", 2, t, 'Hertz', 'Linear')
        f3 = praat.call(formants, "Get value at time", 3, t, 'Hertz', 'Linear')
        fN = f1 * f2 * f3
        if (not math.isnan(fN)) :
          f1_list.append(f1)
          f2_list.append(f2)
          f3_list.append(f3)
          #print("f1 = %.1f" % f1)
          #print("f2 = %.1f" % f2)
          #print("f3 = %.1f" % f3)

    #print("f1 = %.1f" % Average(f1_list))
    #print("f2 = %.1f" % Average(f2_list))
    #print("f3 = %.1f" % Average(f3_list))
    return (Average(f1_list), Average(f2_list), Average(f3_list))

# Now we open the mic and start extract data
# and analyze it

# Microphone initialization
# (avoid error messages at constructor)
err_hand = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
    return
err_handler = err_hand(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
# Set the error handler
asound.snd_lib_error_set_handler(err_handler)
# PyAudio initialization
p = pyaudio.PyAudio()
# (default error handler for the rest of the program)
asound.snd_lib_error_set_handler(None)

# Open the stream
stream=p.open(format=pyaudio.paInt16,channels=1,rate=samplingRate,input=True,
              frames_per_buffer=nSamples) #uses default input device


###############################################
# Create the poitn and move it

x=600
y=600
movingPoints, = plt.plot(x, y, marker='o',color='r')

silence = 0
# moving point
while silence<pausa : 
    data = np.frombuffer(stream.read(nSamples), 'int16')
    result = analyzeSound(data, samplingRate)
    print("%.0f\t%.0f\t%.0f" % (result[0], result[1], result[2]) )
    x = -result[1]
    y = -result[0]
    movingPoints.remove()
    movingPoints, = plt.plot(x, y, marker='o',color='r')
    plt.pause(0.00000000001)
    if x==0 : silence=silence+1
    else : silence=0

# Done 
stream.stop_stream()
stream.close()
p.terminate()

print("Done")


