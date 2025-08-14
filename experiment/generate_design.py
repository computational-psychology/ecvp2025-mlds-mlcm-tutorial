#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate design for one block of MLDS trials
with the method of triads

@author: G. Aguilar, Aug 2025
"""

import itertools
import random

import numpy as np
import pandas as pd

Nblocks = 5

n_realizations = 10


# %% define stimulus vector
stim_vector = np.array([5, 10, 15, 20, 25, 30, 40, 50, 60])
print(stim_vector)

# %%
for nblock in range(1, Nblocks+1):
    
    triads = list(itertools.combinations(stim_vector, 3))
    
    design = []
    for t in triads:
        
        
        r1 = random.choice(range(1, n_realizations+1))
        r2 = random.choice(range(1, n_realizations+1))
        r3 = random.choice(range(1, n_realizations+1))
        
        
        if round(random.random()):
            design.append([t[0], 
                           t[1], 
                           t[2],
                           f"s_{t[0]}_r_{r1}.png",
                           f"s_{t[1]}_r_{r2}.png",
                           f"s_{t[2]}_r_{r3}.png",
                           ])
        else:
            design.append([t[2], 
                           t[1], 
                           t[0],
                           f"s_{t[2]}_r_{r1}.png",
                           f"s_{t[1]}_r_{r2}.png",
                           f"s_{t[0]}_r_{r3}.png",
                           ])
    
    
    df = pd.DataFrame(design, columns = ['s1', 's2', 's3', 'im1', 'im2', 'im3'])
    
    # Shuffle trial order
    df = df.reindex(np.random.permutation(df.index))
    df.reset_index(drop=True, inplace=True)
    df.index.name = "trial"
    
    df.to_csv(f"block_{nblock}.csv")

# %%
