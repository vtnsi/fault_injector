# -*- coding: utf-8 -*-
"""
fault injector test
"""

import numpy as np
import matplotlib.pyplot as plt

from fault_injector.fault_lib import DriftFault
from fault_injector.injector import Injector

x = np.random.normal(size = 500)

# setup fault class
fault_params = {'drift_rate': 0.1}
drift = DriftFault(fault_params)

# setup injector and inject fault
injector_params = {'start': 100, 'stop': 200}
injector = Injector(drift, injector_params)
y = injector.inject_fault(x)


plt.plot(y)