#!/usr/bin/env python3

import math
import parselmouth
from parselmouth import praat
import numpy as np
import pyaudio
from ctypes import *

# Constants for sampling
nSamples = 4096       # number of samples 
samplingRate = 44100  # sampling rate in Hz

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

# Read the mic, convert to numpy array and analyze it with parselmouth
#for i in range(20):
while True :
    data = np.frombuffer(stream.read(nSamples), 'int16')
    # print(data)
    result = analyzeSound(data, samplingRate)
    if result[0] != 0 :
      print(result)

# Done 
stream.stop_stream()
stream.close()
p.terminate()

