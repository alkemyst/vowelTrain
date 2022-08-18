#!/usr/bin/env python3 

import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
plt.xlim(0,1)
plt.ylim(0,1)

# Reference points are drawn here
plt.plot(0,0,marker='o',color='k')

# The moving point (collection) is created here
x=0.5
y=0.5
movingPoints, = plt.plot(x, y, marker='o',color='r')

# moving point
for i in range(200):
    x += (np.random.random()-0.5)/100.
    y += (np.random.random()-0.5)/100.
    if x>1 : x=1
    if x<0 : x=0
    if y>1 : y=1
    if y<0 : y=0
    movingPoints.remove()
    movingPoints, = plt.plot(x, y, marker='o',color='r')
    plt.pause(0.00000000001)

plt.show()


