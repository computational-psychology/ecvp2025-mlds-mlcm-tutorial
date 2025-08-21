#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates stimuli for MLCM experiment on White's illusion

Here we generate all possible images to be presented. 
The script generate_design() creates the exact order to be presented in a block,
randomized.

ECVP 2025 tutorial

@author: G. Aguilar. Aug 2025
"""

from PIL import Image
import itertools
import math
import numpy as np
import matplotlib.pyplot as plt

from stimupy.stimuli import whites


PPD = 34  # Default pixels per degree
BG = 0.5


def generate_stimulus(target_intensities, contexts):
    """
    Generate a White's Illusion stimulus

    Parameters:
    - target_intensities (float, float): Intensity of the target patch (0–1) for
    left and right targets
    - context (int, int): Contexts where the targets are placed, where
        0 for target on a black bar
        1 for target on a white bar

    Returns:
    - numpy array with stimulus, range 0 - 1
    """
    context1, context2 = contexts
    
    target_indices = (6 + context1, 12 + context2)
        
    
    # Generate White's Illusion stimulus
    illusion = whites.white(
        visual_size=(12, 16),       # Visual size in degrees
        ppd=PPD,                   # Pixels per degree
        n_bars=18,                 # Number of bars
        origin="corner",           # Center the stimulus at the origin
        intensity_bars=(0.0, 1.0), # Intensity of the bars
        target_indices=target_indices,  # Target bar index
        target_heights=5,          # Height of the target bar
        intensity_target=target_intensities  # Intensity of the target patch
    )
    
    im = illusion["img"][:, :-7]  # Crops last columns
    
    # Adds markers on the bottom
    markers = np.ones((30, im.shape[1]))*BG
    
    mask = illusion['target_mask'].astype(float)
    line = mask[int(mask.shape[0]/2), :-7]
    i1 = np.where(line==0)
    i2 = np.where(line==1)
    i3 = np.where(line==2)
    line[i1] = BG
    line[i2] = 0
    line[i3] = 0
    
    markers[20:30, :] = line
        
    #targets_xmask = 0.2 * (illusion["target_mask"][int(illusion["target_mask"].shape[0] / 2), :] == 0)
    #targets_xmask = targets_xmask.reshape(1, len(targets_xmask))
    #marker_img = np.repeat(targets_xmask, 10, axis=0)
    
    return np.vstack((im, markers))

    
# %% Testing stimulus generation
img00 = generate_stimulus((0.5, 0.5), (0, 0))
img10 = generate_stimulus((0.5, 0.5), (1, 0))
img01 = generate_stimulus((0.5, 0.5), (0, 1))
img11 = generate_stimulus((0.5, 0.5), (1, 1))

fig, axes = plt.subplots(2, 2, figsize=(8,8))
axes[0][0].imshow(img00, cmap='gray')
axes[0][0].set_title('black - black')
axes[0][1].imshow(img01, cmap='gray')
axes[0][1].set_title('black - white')
axes[1][0].imshow(img10, cmap='gray')
axes[1][0].set_title('white - black')
axes[1][1].imshow(img11, cmap='gray')
axes[1][1].set_title('white - white')
plt.show()


# %% define first stimulus dimension. in this case relative luminace
#lum_vector = np.array([0.01, 0.035, 0.07, 0.131, 0.26, 0.39, 0.52, 0.64, 0.77, 0.9])
#lum_vector = np.linspace(0.1, 0.9, 10).round(2)
lum_vector = np.linspace(0.25, 0.75, 7).round(2)
print(lum_vector)

contexts = [0.0, 1.0] # second stimulus dimension


# %% we now  create all possible pairwise combinations

stimuli = [(lum, c) for lum in lum_vector  for c in contexts]

stimuli_design = list(itertools.combinations(stimuli, 2))


for s in stimuli_design:
    print(f"generating {s}")
    lum1, context1 = s[0]
    lum2, context2 = s[1]
    
    # we fist create and save the stimulus with order left-right
    img = generate_stimulus((lum1, lum2), (context1, context2))
    im = Image.fromarray(img*255).convert('L')
    im.save(f"imgs/white_{lum1}_{lum2}_{context1}_{context2}.png")
    
    # and now we create the version right-left
    img = generate_stimulus((lum2, lum1), (context2, context1))
    im = Image.fromarray(img*255).convert('L')
    im.save(f"imgs/white_{lum2}_{lum1}_{context2}_{context1}.png")    
    
    
