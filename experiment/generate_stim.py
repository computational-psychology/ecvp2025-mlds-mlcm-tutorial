#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates stimuli for numerosity MLDS experiment

ECVP 2025 tutorial

@author: G. Aguilar. Aug 2025
"""

import random
import math
import numpy as np
import matplotlib.pyplot as plt


def distance(x, y):
    return np.sqrt(np.sum((x-y)**2, axis=1))


def random_point_in_circle(radius=1, center=(0, 0)):
    """
    Generates a random point (x, y) uniformly within a circle.

    Args:
        radius: The radius of the circle.
        center: A tuple (x_center, y_center) representing the circle's center.

    Returns:
        A tuple (x, y) representing the random point.
    """
    r = radius * math.sqrt(random.random())
    theta = 2 * math.pi * random.random()
    x = center[0] + r * math.cos(theta)
    y = center[1] + r * math.sin(theta)
    return np.array([x, y])[np.newaxis, :]


def get_coordinates_stimulus(number_dots, min_d):
    """
    Generates the x-y coordinates of the stimulus' cloud of dots, 
    randomly samples from a circle.
    The function checks that the dots do not overlap considering the argument
    min_d

    Args:
        number_dots: The total number of dots
        min_d: Minimum distance among dots

    Returns:
        A vector (number_dots, 2) representing the x-y coordinates
    """

    # initialize first dot at random position in range 0-1
    #xy = np.random.uniform(size=(1, 2))
    xy = random_point_in_circle()
    
    for n in range(s-1):
    
        found = False
        while not found:
            #newpos = np.random.uniform(size=(1, 2))
            newpos = random_point_in_circle()
    
            # check overlap
            d = distance(xy, newpos)
    
            if np.all(d > min_d):
                found = True
    
        # if do not overlap, append
        xy= np.vstack((xy, newpos))

    return xy
    

def create_stimulus(xy):
    
    # create stimulus as scatterplot
    fig, axes = plt.subplots(1, 1, figsize=(4, 4))
    fig.patch.set_facecolor((0.5, 0.5, 0.5))
    axes.scatter(xy[:, 0], xy[:, 1], c=color, s=100)
    axes.set_xlim([-1.1, 1.1])
    axes.set_ylim([-1.1, 1.1])
    #axes.set_facecolor((0.5, 0.5, 0.5))
    axes.set_axis_off()
    plt.tight_layout()
    
    
    return fig

# %%

n_realizations = 5

# minimum distance between dots. This is used to avoid overlapping
min_d = 0.125
color = 'k'


# %% define stimulus vector
#stim_vector = np.linspace(0, 2, 10).round().astype(int)
stim_vector = np.array([5, 10, 15, 20, 25, 30, 40, 50, 60])
print(stim_vector)


# iterate along stimuli
for s in stim_vector:
    # do n realizations
    for nr in range(n_realizations):
        xy = get_coordinates_stimulus(s, min_d)
    
        fig = create_stimulus(xy)
        
        fig.savefig(f"imgs/s_{s}_r_{nr+1}.png")
        plt.close(fig)

