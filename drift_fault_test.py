# -*- coding: utf-8 -*-
"""
drift fault test
"""

import numpy as np
import matplotlib.pyplot as plt

from fault_injector.fault_lib import DriftFault

x = np.random.normal(size = 100)


params = {'drift_rate': 0.1}
f = DriftFault(params)
y = f(x)

plt.plot(y)