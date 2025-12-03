# -*- coding: utf-8 -*-
"""
base fault class
"""
import numpy as np
import matplotlib.pyplot as plt


class BaseFault:
    """
    BaseFault
    ---------

    """
    def __init__(self):

        self.name = 'base_fault'


    def __call__(self, x):

        return x
