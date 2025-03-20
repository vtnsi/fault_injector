# Fault_Injection

## Introduction
Fault_Injection is designed inject faults into sensor data. The fault options include:
- Drift
- Offset
- No Output (NaN)
- Stuck Value
- Noise: gaussian
- Noise: uniform

## Install & Import
### Add to Environment
In environment terminal:
```
pip install pip install git+https://github.com/vtnsi/fault_injector.git
```

### Import
```py
import fault_injector.generate_data as gd
import fault_injector.injector as injector
```

## Demo
The `demo.ipynb` file can be used as a demonstration, including an example for all the faults.

## Generate Synthetic Data
The `DataGen` class in `generate_data.py` file can be used to generate a list of synthetic sensor data. This data would represent the sensor data prior to injecting a fault. `DataGen` takes in three values:
- `rand_max`: positive, numeric value
- `rand_min`: positive, numeric value
- `size`: positive integer

Here's an example of generating a DataFrame of synthetic data:
```py
# generate synthetic data
gen_dict = {}
def gen_values(rand_max, rand_min, size):
    gen = gd.DataGen(rand_max, rand_min, size)
    gen.random_gen()
    return gen.values

gen_dict['x'] = gen_values(0.52, 0.48, 1000)
gen_dict['y'] = gen_values(8100, 7900, 1000)
gen_dict['z'] = gen_values(1.1, 0.9, 1000)

df = pd.DataFrame(gen_dict)
```

For more example of working with `DataGen`, check out `demo.ipynb`.

## Fault Injector Class
The `FaultInjection` class in `injector.py` is the main class for this package. The class can be used to inject fault(s) during a designated time period. The class takes in:
- `values`: a **list** of numeric values
- `start`: Specifies the starting time for the fault. By default, it is set to `None`, which initializes it to `0`.
  - If set to `"random"`, a random starting point is generated between `0` and half of the length of the values.
  - If given as an integer, it must be between `0` and the length of the values.
  - If the provided integer is greater than or equal to the length of the values, `start` is set to the last valid index.
- `stop`: Specifies the ending time for the fault. By default, it is set to `None`, which initializes it to the length of the values.
  - If set to `"random"`, a random ending point is generated between `start` and the length of the values.
  - If given as an integer, it must be at least one more than `start` and at most the length of the values.
  - If the provided value exceeds the length of the values, it is capped at the maximum valid index.
- `increasing`: a binary value (0 or 1). 1 will cause the fault to increase the values and 0 will decrease the values.

*Note: to randomly generate a start/end, set the variable to `-1`*

Faults and their corresponding function:
- Drift: `inject_drift()`
- Offset: `inject_offset()`
- No Output (NaN): `inject_nan()`
- Stuck Value: `inject_stuck_value()`
- Noise (gaussian): `inject_noise(noise_type='gaussian')`
- Noise (uniform): `inject_noise(noise_type='uniform')`

*Note: `inject_stuck_value()` will generate a random stuck value unless the stuck value is specified. For example: `inject_stuck_value(stuck_val = 0.8)`*

### Additional Functions
* `plot_compare_values()`: plots both the original values and the faulty data.
* `restore_values()`: this function will revert the data back to the original values.

## Inject Faults into A DataFrame
As mentioned previously, the `FaultInjection` class is designed to inject faults into lists. If you are using data frames, use the `DataFrameFaultInjection` class. This class allows you to use the `FaultInjection` on a data frame. It takes in:
- `df`: this should be a pandas data frame
- `column_names`: this can be a single string or a list of strings corresponding to column names in `df`
- `start_val`: dictate the starting time for the fault. It should be a positive integer that is less than the length of the values
- `stop_val`: dictate the ending time for the fault. It should be an integer that is larger than start, but less than the length of the values

### Inject Fault into DataFrame
The output of the `inject_fault` function in `DataFrameFaultInjection` is a dictionary. The keys correspond to the strings in `column_names`. This function initializes a `FaultInjection` class object for every key. This makes it so the user can utilize all of the functions available in the `FaultInjection` class.

For example, this would allow you to inject an offset fault in all of the specified columns:
```py
inject_fault_df = df_injector.DataFrameFaultInjection(df, column_names=col_lst, start_val=start_val, stop_val=stop_val)
fault_dict = inject_fault_df.inject_fault()

for key in fault_dict.keys():
    print(key)
    fault_dict[key].inject_offset()
    fault_dict[key].plot_compare_values()
```

### Update DataFrame
The `update_df` function can be used to take the faulty data and update the data in the original data frame. This can be used when the user only injects faults into some of the columns.
