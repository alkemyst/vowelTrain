#!/usr/bin/env python3

import math
import parselmouth
from parselmouth import praat

testFiles = [ 'Close_back_rounded_vowel', 'Close_back_unrounded_vowel', 
              'Close_central_rounded_vowel', 'Close_central_unrounded_vowel', 
              'Close_front_rounded_vowel', 'Close_front_unrounded_vowel', 
              'Close-mid_front_unrounded_vowel', 'Mid-central_vowel', 
              'Near-close_near-back_rounded_vowel', 'Near-close_near-front_rounded_vowel',
              'Near-close_near-front_unrounded_vowel', 'Open-mid_front_rounded_vowel', 
              'PR-open_back_rounded_vowel', 'PR-open-mid_back_rounded_vowel' ]

def Average(arr) :
    return sum(arr)/len(arr)


def analyzeVowel(testFile):
    testFileName = "samples/" + testFile + ".wav"
    sound = parselmouth.Sound(testFileName) 
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
    #print("f1 = %.1f" % Average(f1_list))
    #print("f2 = %.1f" % Average(f2_list))
    #print("f3 = %.1f" % Average(f3_list))
    testFile.replace('.*/', '')
    print("%s, %.1f, %.1f, %.1f" % (testFile, Average(f1_list), Average(f2_list), Average(f3_list)))

for aFile in testFiles:
    analyzeVowel(aFile)

