#!/usr/bin/env python3

import math
import parselmouth
from parselmouth import praat
import numpy as np

def Average(arr) :
    return sum(arr)/len(arr)

def analyzeSound():
    # Vector constructor listed here
    # https://parselmouth.readthedocs.io/en/stable/api_reference.html#parselmouth.Sound.__init__
    sound = parselmouth.Sound(np.sin(2 * np.pi * 440 * np.arange(48000) / 48000), sampling_frequency=48000)
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


print (analyzeSound())

