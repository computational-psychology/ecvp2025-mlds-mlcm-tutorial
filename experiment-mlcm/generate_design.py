#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate design for one block of trials for the MLCM experiment on 
White's illusion 

@author: G. Aguilar, Aug 2025
"""

import itertools
import random
import numpy as np
import pandas as pd

Nblocks = 5

reduced = False

# %% define stimulus vector for dimension 1, in this case, relative luminance
#stim_vector_1 = np.linspace(0.1, 0.9, 7).round(2)
stim_vector_1 = np.linspace(0.25, 0.75, 7).round(2)
print(stim_vector_1)

# now define the stimulus vector for dimension 2.
# in this case it is either a target on top of a black or white bar
stim_vector_2 = np.array([0.0, 1.0]) 

# %%
stimuli = [(lum, c) for lum in stim_vector_1  for c in stim_vector_2]
stimuli_design = list(itertools.combinations(stimuli, 2))


# we only present trials across-contexts, but two times
if reduced: 
    for s in stimuli_design:
        if s[0][1]==s[1][1]:
            stimuli_design.remove(s)
            
    stimuli_design  = stimuli_design*2
    
   
for nblock in range(1, Nblocks+1):
        
    design = []
    
    for s in stimuli_design:
        
               
        if round(random.random()):  
            lum_left, context_left = s[0]
            lum_right, context_right = s[1]
            
        else:
            lum_right, context_right = s[0]
            lum_left, context_left = s[1]
            
        
                
        
        design.append([lum_left, 
                       lum_right, 
                       context_left,
                       context_right,
                       f"imgs/white_{lum_left}_{lum_right}_{context_left}_{context_right}.png",
                       ])
    
    
    df = pd.DataFrame(design, columns = ['lum1', 'lum2', 'c1', 'c2', 'im'])
        
    # Shuffle trial order
    df = df.reindex(np.random.permutation(df.index))
    df.reset_index(drop=True, inplace=True)
    df.index.name = "trial"
    
    df.to_csv(f"block_{nblock}.csv")

# %%
