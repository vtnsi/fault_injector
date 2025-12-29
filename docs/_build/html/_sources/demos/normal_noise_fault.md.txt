# Normal Noise Fault Demo

This tutorial will walk you through:

- creating a fault instance
- creating an injector instance
- using the injector to inject a fault into data
- visualize the results

## Setup and import packages

Import NormalNoiseFault and other packages that are used in this tutorial

```python
import sys
import os

# Add the repo root to sys.path
repo_root = os.path.abspath("..")
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from fault_injector.generate_data import DataGen
from fault_injector.injector import Injector
from fault_injector.visualizer import FaultVisualizer
from fault_injector.fault_lib import *
import numpy as np
import matplotlib.pyplot as plt
```

## Starting Data

Generate random generated data using the `DataGen` library. This data will serve as the sensor data for this experiment.

Any list or array of numeric values can replace the `original_value` variable in this tutorial.

```python
rand_max = 0.52
rand_min = 0.48
size = 500

# create class object
gen_obj = DataGen(rand_max, rand_min, size)

# generate synthetic data
gen_obj.random_gen()
original_values = np.array(gen_obj.values)
gen_obj.plot_values()
```

Generated Data

![original](../../images/demos/normal_noise_fault/original.png)


## Define Fault

This example will utilize the `NormalNoiseFault` library to create an instance of the normal noise fault. The `NormalNoiseFault` expects the `params` variable to be equal to a dictionary containing the keys `mu` and `sigma`.

For more information as to how `mu` and `sigma` are used, please see the `loc` and `scale` variable in the Numpy random.normal documentation, [found here](https://numpy.org/doc/2.1/reference/random/generated/numpy.random.normal.html)

```python
fault_params = {"mu": 0,
                "sigma": 0.1}
fault_obj = NormalNoiseFault(params=fault_params)
```

## Define Injector

The `Injector` library will be used for the injector instance. This instance take in `fault` and `params`.

`fault` expects a fault object, just like the one created in the previous step.

`params` expects a dictionary with two keys: `start` and `stop`. These keys correspond to the starting and ending indices for the list/array of numeric values that will receive the fault. In this example, the indices that receive the fault range from 100 to 400.

```python
injector_params = {"start":100,
                   "stop": 400}
injector_object = Injector(fault=fault_obj,
                           params=injector_params)
```

## Inject Fault

Use the `inject_fault` method of the `Injector` object to inject the fault. This method expects the `x` variable to be set equal to a list or array of numeric values. This represents the true values prior to receiving a fault. For this example, the `original_values` variable that was generated earlier will be used.

```python
new_values = injector_object.inject_fault(x=original_values)
```

## Compare Original to New Values

To visualize the fault, we will examine the Fault delta, then plot the new values compared to the true values.

```python
# initiate the visualizer
vis = FaultVisualizer()

vis.plot_fault_delta(original_values, new_values, title='Fault Delta')
```

Fault Delta

![delta](../../images/demos/normal_noise_fault/delta.png)

```python
vis.plot_comparison(original_values, new_values, title='Comparison')
```

Fault Comparison

![comparison](../../images/demos/normal_noise_fault/comparison.png)
