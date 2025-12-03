# -*- coding: utf-8 -*-
"""
drift fault test
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from fault_injector.fault_lib import DriftFault
from fault_injector.injector import Injector
from fault_injector.df_injector import DataFrameInjector


# test data
df = pd.DataFrame({'Col1': np.random.normal(size = 500),
                   'Col2': np.random.normal(size = 500),
                   'Col3': np.random.normal(size = 500)})

# setup fault class
fault_params1 = {'drift_rate': 0.1}
drift1 = DriftFault(fault_params1)

fault_params2 = {'drift_rate': 0.2}
drift2 = DriftFault(fault_params2)

# setup injector
injector_params = {'start': 100, 'stop': 200}

# setup dataframe injector
df_dict = {'Col1': Injector(drift1, injector_params), 'Col2': Injector(drift2, injector_params)}
df_injector = DataFrameInjector(df_dict)
df_faulty = df_injector.inject_faults(df)
df_faulty.plot()