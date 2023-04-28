#!/usr/bin/env python

import numpy as np
from roboticstoolbox import DHRobot, SerialLink, DHLink
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

a_0 = 0.1
a_1 = 0.1
a_2 = 0.1
a_3 = 0.1
a_4 = 0.1
a_5 = 0.1
a_6 = 0.05

# Create a list of links
links = [ \
         DHLink(alpha=np.pi/2,        a=0,  d=0.,   theta=-np.pi/2,         sigma=1),  \
         DHLink(alpha=0,              a=-a_1,  d=0.,   theta=0,         sigma=0),  \
         DHLink(alpha=np.pi/2,        a=0,  d=a_2,   theta=0,         sigma=0),  \
         DHLink(alpha=np.pi/2,        a=0,  d=a_3,   theta=0,         sigma=0),  \
         DHLink(alpha=np.pi,          a=0,  d=0,   theta=0,         sigma=0),  \
         ]

# Theta
q0 = np.zeros(len(links)) 
if len(q0) > 2:
    q0[2] = np.pi/2
# q0[4] = -np.pi/2

# Create a DHRobot object using the list of links
robot = DHRobot(links)

# Create a SerialLink object from the DHRobot object
robot_link = SerialLink(links)

# Define the initial joint configuration for the robot
q = q0

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define the slider axes
slider_axes = []
cnt = -1
ignore = [0, 2, 4,  7]
for i in range(len(q0)):
    offset = 0
    if i in ignore:
        offset = 500
    else:
        cnt = cnt + 1
    slider_ax = plt.axes([0.7 + offset, 0.1 + cnt*0.03, 0.2, 0.03])
    slider_axes.append(slider_ax)

# Define the sliders
sliders = []
for i in range(len(q0)):
    slider = Slider(slider_axes[i], f'q{i+1}', -np.pi, np.pi, valinit=q0[i], zorder=10)
    sliders.append(slider)

# Update the robot when the slider values are changed
def update(val):
    q = np.array([slider.val for slider in sliders])
    robot_link.plot(q, block=False, fig=fig, dt=1.0)

# Connect the sliders to the update function
for slider in sliders:
    slider.on_changed(update)

# Visualize the robot in a GUI window
robot_link.plot(q, block=True, fig=fig, dt=1.0)
