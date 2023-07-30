#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


class ray:
    def __init__(self):
        self.r = np.array([0,0,0])  # position 
        self.s = np.array([0,0,0])  # direction cosine 
        # self.eikonal = 0;