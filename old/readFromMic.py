#!/usr/bin/env python3

import numpy as np
import pyaudio
from ctypes import *

nSamples = 4096       # number of samples 
samplingRate = 44100  # sampling rate in Hz

# Avoid error messages at constructor 
err_hand = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
    return
err_handler = err_hand(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
# Set the error handler
asound.snd_lib_error_set_handler(err_handler)
# PyAudio initialization
p = pyaudio.PyAudio()
# Default error handler for the rest of the program
asound.snd_lib_error_set_handler(None)

# Open the stream
stream=p.open(format=pyaudio.paInt16,channels=1,rate=samplingRate,input=True,
              frames_per_buffer=nSamples) #uses default input device

# Read and convert to numpy array 
for i in range(5):
    data = np.frombuffer(stream.read(nSamples), 'int16')
    print(data)

# Done 
stream.stop_stream()
stream.close()
p.terminate()
