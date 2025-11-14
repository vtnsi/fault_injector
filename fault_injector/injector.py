import random
import matplotlib.pyplot as plt
import numpy as np

class FaultInjection:
    r"""
    FaultInjection(values, start=None, stop=None, increasing=0)

    A class for injecting various faults into a numeric time-series or sensor data.

    This class allows simulation of real-world sensor anomalies including
    drift, offset, noise, missing data, and stuck readings. Faults can be
    applied over a specified range of indices.

    .. rubric:: Parameters:

    **values** : *list of float or int*
        The original numeric values to inject faults into.
    **start** : *int or 'random', optional*
        Start index of the fault (default 0). If 'random', a random start is selected.
    **stop** : *int or 'random', optional*
        Stop index of the fault (default: length of values). Must be greater than start.
    **increasing** : *int (0 or 1), optional*
        Determines fault direction: 1 = increase values, 0 = decrease values (default 0).


    .. rubric:: Supported Fault Types

    1. **Drift**:
       Linear change over time

    2. **Offset**:
       Constant bias added to the values

    3. **Gaussian Noise**:
       Random noise with normal distribution

    4. **Uniform Noise**:
       Random noise with uniform distribution

    5. **NaN**:
       Replace values with missing data

    6. **Stuck Value**:
       Replace values with a constant

    Notes
    -----
    - Faults are applied over the range [start, stop).
    - The class preserves the original values for comparison.
    - Useful for testing robustness of sensor data processing algorithms,
      anomaly detection, and fault-tolerant systems.
    """
    def __init__(self, values, start=None, stop=None, increasing=0):
        r"""
        The FaultInjection class is designed to take in a list of numeric values and inject a fault into the values

        Args:
            values: a list of numeric values
            start: defines the starting time for the fault and corresponds with the index values for the elements in the list.
                - It must be a non-negative integer less than the length of the values.
                - "random" can be used to generate a random starting value.
                - Defaults to None.
            stop: defines the ending time for the fault and corresponds with the index values for the elements in the list.
                - It must be a non-negative integer less than the length of the values and greater than the 'start' value.
                - 'random' can be used to generate a random ending value.
                - Defaults to None.
            increasing: should be a binary value (0 or 1).
                - 1 will cause the fault to increase the values.
                - 0 will decrease the values.
                - Defaults to 0.
        """

        try:
            # Check if it's a non-empty list
            if not isinstance(values, list) or not values:
                raise ValueError("Invalid Input (values): \n values must be a non-empty list of numbers.")

            # Check the type of the first element in the list
            if not isinstance(values[0], (float, int, np.int64)):
                raise ValueError("Invalid Input (values): \n values must be a list of numbers.")

            # find the maximum possible length of the fault
            self.max_end = len(values)

            # this variable will receive the fault injection
            self.values = values.copy()

            # the original values will be preserved and can be used for comparison
            self.original_values = values.copy()

            # calculate the average value
            self.original_average = np.average(self.original_values)

            # Validate 'start'
            if start is None:
                self.start = 0
            elif start == "random":
                self.start = random.randint(0, self.max_end // 2)
            elif isinstance(start, int) and start >= 0:
                self.start = min(start, self.max_end - 1)
            else:
                raise ValueError(
                    "Invalid Input (start): \n It must be either:\n"
                    " - An integer between 0 and the length of values.\n"
                    " - 'random' to generate a random starting point.\n"
                    " - None to default to 0."
                )

            # Validate 'stop'
            if stop is None:
                self.stop = self.max_end
            elif stop == "random":
                self.stop = random.randint(self.start + 1, self.max_end)
            elif isinstance(stop, int) and stop >= 0:
                self.stop = min(max(self.start, stop), self.max_end)
            else:
                raise ValueError(
                    "Invalid Input (stop): \n 'stop' must be an integer between 'start' and the length of values,\n"
                    "or 'random' to generate a random endpoint.\n"
                    "Set to None to default to the length of values."
                )

            # Validate 'increasing'
            if increasing in {0, 1}:
                self.fault_direction = 1 if increasing == 1 else -1
            else:
                raise ValueError("Invalid Input (increasing): \n increasing must be 0 or 1.")
            # define the fault length
            self.fault_length = self.stop - self.start

        except ValueError as e:
            print(f"Error: {e}")

    def restore_values(self):
        r"""
        This will revert values back to the original state
        """

        self.values = self.original_values.copy()

    def inject_fault(self, change_lst:list):
        """This is a generic method that can be used to add custom faults to the original values.
        It takes in a list of numeric values that will be added to the existing values.
        For example, this method is used by the `inject_drift` method to add the drift values to the existing values.

        Note: this method is used to add values to the existing values **not** replace the existing values.

        Args:
            change_lst (list): a list of numeric values
        """
        # placeholder for unchanged values
        fault_lst = [0] * self.start

        # add fault change
        fault_lst.extend(change_lst)

        # place holder for unchanged ending values
        unchanged_end_lst = [0] * (self.max_end - self.stop)

        # combine lists
        fault_lst.extend(unchanged_end_lst)

        # add change to values
        self.values = np.array(self.values) + np.array(fault_lst)

        # convert back to a list
        self.values = list(self.values)


    def inject_drift(self, drift_rate=None):
        r"""
        Injects a linear drift into the signal over the fault range.

        .. rubric:: Parameters:

        **drift_rate** : *float, optional*
            The rate of change per step. If not provided,
            a random small value    is generated as:

            .. math::
                \text{drift_rate} = U(0, 0.0001) \times d \times \bar{x}


            where:
                - :math:`U(a,b)` is a uniform random number in [a, b]
                - :math:`d` is the fault direction (+1 for increasing, -1 for decreasing)
                - :math:`\bar{x}` is the mean of the original values

        .. admonition:: Math behind Drift Fault

            The drift increases (or decreases) linearly with time:

            .. math::
                y_i = x_i + (i - s) \cdot \text{drift_rate}, \quad i \in [s, e)


            where:
                - :math:`x_i` = original value
                - :math:`y_i` = value after drift
                - :math:`s` = start index
                - :math:`e` = stop index


            **Impact on Descriptive Statistics (within [s, e))**

                - **Mean:**

                The mean of the faulted segment increases (or decreases) linearly by half the
                total drift span:

                .. math::
                    \bar{y}_{[s,e)} = \bar{x}_{[s,e)} + \frac{(e - s - 1)}{2} \cdot \text{drift_rate}


                - **Variance:**

                The added linear trend increases variance quadratically with the fault length:

                .. math::
                    \text{Var}(y_{[s,e)}) = \text{Var}(x_{[s,e)}) + \frac{(e - s)^2 - 1}{12} \cdot \text{drift_rate}^2

        """
        try:
            if drift_rate == None:
                # generate a random drift rate
                drift_rate = random.uniform(0, 0.0001) * self.fault_direction * self.original_average
            elif not isinstance(drift_rate, (float, int, np.int64)):
                raise ValueError("drift_rate needs to be a float or int")
            self.drift_rate = drift_rate
        except ValueError as e:
            print(f"Error: {e}")

        # list of values that equal the amount of change during the fault injection
        change_lst = list(np.array(range(1, self.fault_length + 1)) * self.drift_rate)

        self.inject_fault(change_lst)


    def inject_offset(self, offset_rate=None):
        r"""
        Injects a constant offset (bias) into the signal over the specified fault range.

        .. rubric:: Parameters:

        **offset_rate** : *float, optional*
            Fraction of the mean value to use as the offset magnitude.
            If not provided, a random offset is generated:

            .. math::
                \text{offset_rate} \sim U(0.01, 0.1)

            The actual offset value is computed as:

            .. math::
                \text{offset_value} = \bar{x} \cdot \text{offset_rate}


            where:
                - :math:`U(a,b)` is a uniform random value in [a, b]
                - :math:`\bar{x}` is the mean of the original (fault-free) values

        .. admonition:: Math behind Offset Fault

            The offset fault adds a constant bias to all values between the fault
            start and stop indices:

            .. math::
                y_i =
                \begin{cases}
                x_i + \text{offset_value}, & \text{if } s \le i < e \\
                x_i, & \text{otherwise}
                \end{cases}


            where:
                - :math:`x_i` = original value
                - :math:`y_i` = value after offset fault
                - :math:`s` = start index
                - :math:`e` = stop index


            **Impact on Descriptive Statistics (within [s, e))**

                - **Mean:**

                The mean shifts by the offset magnitude:

                .. math::
                    \bar{y}_{[s,e)} = \bar{x}_{[s,e)} + \text{offset_value}

                - **Variance:**

                Variance remains unchanged since a constant shift does not alter spread:

                .. math::
                    \text{Var}(y_{[s,e)}) = \text{Var}(x_{[s,e)})


        The offset direction depends on the `increasing` flag provided at initialization.
        If `increasing=1`, the offset is positive; if `increasing=0`, the offset is negative.


        Notes
        -----
        Offset faults model **sensor bias** or **systematic calibration error**, where
        readings remain accurate in trend but are consistently higher or lower than
        true values.
        """
        try:
            if offset_rate == None:
                offset_rate = random.uniform(0.01, 0.1)
            elif not isinstance(offset_rate, (float, int, np.int64)):
                raise ValueError("offset_rate needs to be a float or int")
        except ValueError as e:
            print(f"Error: {e}")
        self.offset_rate = self.original_average * offset_rate

        # list of values that equal the amount of change during the fault injection
        change_lst = [self.offset_rate] * self.fault_length

        self.inject_fault(change_lst)


    def inject_nan(self):
        r"""
        Replaces all values within the fault range with NaN (Not a Number).

        This simulates data loss, sensor dropout, or transmission failure,
        where no valid measurement is available for a period of time.

        .. admonition:: Math behind Nan Fault

            All values between the fault start and stop indices are set to NaN:

            .. math::
                y_i =
                \begin{cases}
                \text{NaN}, & \text{if } s \le i < e \\
                x_i, & \text{otherwise}
                \end{cases}


            where:
                - :math:`x_i` = original value
                - :math:`y_i` = value after fault injection
                - :math:`s` = start index
                - :math:`e` = stop index


            **Impact on Descriptive Statistics (within [s, e))**

                - **Mean / Variance:**

                Undefined within the faulted region because all values are NaN.
                In most statistical analyses, these samples are excluded, effectively
                reducing the sample size.

        Notes
        -----
        This fault type is commonly used to simulate missing data segments in
        time series or sensor readings due to disconnection, corruption, or
        transmission errors.
        """
        # list of NaN values
        change_lst = [np.nan] * self.fault_length

        self.values[self.start:self.stop] = change_lst


    def inject_stuck_value(self, stuck_val=None):
        r"""
        Replaces all values within the fault range with a constant "stuck" value.

        This simulates a sensor fault where the output remains frozen at a fixed
        reading, regardless of the true input signal.

        .. rubric:: Parameters:

        **stuck_val** : *float, optional*
            The constant value to use during the fault period.
            If not provided, a random stuck value is generated as:

            .. math::
                \text{stuck_val} = \bar{x} + d \cdot U(0.01, 0.1) \cdot \bar{x}

            where:
                - :math:`U(a,b)` is a uniform random number in [a, b]
                - :math:`d` is the fault direction (+1 for increasing, -1 for decreasing)
                - :math:`\bar{x}` is the mean of the original values


        .. admonition:: Math behind Stuck Value Fault

            All values between the fault start and stop indices are replaced by a
            single constant:

            .. math::
                y_i =
                \begin{cases}
                c, & \text{if } s \le i < e \\
                x_i, & \text{otherwise}
                \end{cases}


            where:
                - :math:`x_i` = original value
                - :math:`y_i` = value after fault injection
                - :math:`c` = stuck value
                - :math:`s` = start index
                - :math:`e` = stop index


            **Impact on Descriptive Statistics (within [s, e))**

                - **Mean:**

                The mean becomes equal to the stuck constant:

                .. math::
                    \bar{y}_{[s,e)} = c

                - **Variance:**

                All values are identical, so variance collapses to zero:

                .. math::
                    \text{Var}(y_{[s,e)}) = 0


        Notes
        -----
        This fault type is useful for modeling sensor freezing, where a device
        stops updating and continuously outputs the same measurement.
        """
        # check stuck_val input
        try:
            if stuck_val is None:
                stuck_val = random.uniform(0.01, 0.1) * self.fault_direction * self.original_average + self.original_average
            elif not isinstance(stuck_val, (int, float, np.int64)):
                raise ValueError("stuck_val needs to be a float or an int. To generate a random stuck_val, set to None")
        except ValueError as e:
            print(f"Error: {e}")
        # list of stuck values
        change_lst = [stuck_val] * self.fault_length

        self.values[self.start:self.stop] = change_lst


    def inject_noise(self, noise_type, params=None):
        r"""
        Injects random noise into the signal over the fault range.

        This simulates measurement noise or sensor variability, and supports
        two types of noise distributions: Gaussian (normal) and Uniform.

        .. rubric:: Parameters:

        **noise_type** : *str*
            Type of noise to inject. Must be either ``"gaussian"`` or ``"uniform"``.

        **params** : *list, optional*
            Parameters defining the noise distribution.

            - **Gaussian:** `[mu, sigma]`
                - `mu` = mean of the noise (default: 0)
                - `sigma` = standard deviation (default: std of values[start:stop])

            - **Uniform:** `[low, high]`
                - `low` = lower bound (default: -std of values[start:stop])
                - `high` = upper bound (default: std of values[start:stop])

        .. admonition:: Math behind Noise Fault

            The values are perturbed by random noise:

            - **Gaussian noise**:

            .. math::
                y_i = x_i + \epsilon_i, \quad
                \epsilon_i \sim \mathcal{N}(\mu, \sigma^2), \quad i \in [s, e)

            - **Uniform noise**:

            .. math::
                y_i = x_i + \epsilon_i, \quad
                \epsilon_i \sim U(a, b), \quad i \in [s, e)

            where:
                - :math:`x_i` = original value
                - :math:`y_i` = value after noise injection
                - :math:`s` = start index
                - :math:`e` = stop index
                - :math:`\mathcal{N}(\mu, \sigma^2)` = normal distribution
                - :math:`U(a, b)` = uniform distribution in [a, b]

            **Gausian Noise Fault: Impact on Descriptive Statistics (within [s, e))**

                - **Mean:**

                Expected mean remains approximately unchanged if :math:`\mu = 0`:

                .. math::
                    \mathbb{E}[\bar{y}_{[s,e)}] = \bar{x}_{[s,e)} + \mu

                - **Variance:**

                Total variance increases additively by noise variance:

                .. math::
                    \text{Var}(y_{[s,e)}) = \text{Var}(x_{[s,e)}) + \sigma^2


            **Uniform Noise Fault: Impact on Descriptive Statistics (within [s, e))**

                - **Mean:**

                Expected mean shifts by the midpoint of the uniform range:

                .. math::
                    \mathbb{E}[\bar{y}_{[s,e)}] = \bar{x}_{[s,e)} + \frac{a + b}{2}

                - **Variance:**

                Variance increases by the variance of the uniform noise:

                .. math::
                    \text{Var}(y_{[s,e)}) = \text{Var}(x_{[s,e)}) + \frac{(b - a)^2}{12}.


        Variance increases by the variance of the uniform noise.

        ---

        Notes
        -----
        This fault type is useful for simulating **sensor variability**, **environmental interference**, or **random jitter** in measurements.
        """
        if params is None:
            params = []
        try:
            if not isinstance(params, list):
                raise ValueError("params needs to be a list")
            elif noise_type == 'gaussian':
                if len(params) == 0:
                    # calculate mean
                    params.append(0)
                    # calculate standard deviation
                    params.append(np.std(self.values[self.start:self.stop]))
                elif len(params) > 2 or len(params) == 1:
                    raise ValueError("""Params should either be an empty list or it should contain 2 elements.
                                    \nThe values will be used in np.random.normal(params[0], params[1], fault_length)
                                    \nparams[0] typically represents the mean of the distribution
                                    \nparams[1] typically represents the standard deviation""")

                change_lst = np.random.normal(params[0], params[1], self.fault_length)
                self.values[self.start:self.stop] += change_lst

            elif noise_type == 'uniform':
                if len(params) == 0:
                    # calculate min value
                    params.append(-1 * np.std(self.values[self.start:self.stop]))
                    # calculate max value
                    params.append(np.std(self.values[self.start:self.stop]))
                elif len(params) > 2 or len(params) == 1:
                    raise ValueError("""Params should either be an empty list or it should contain 2 elements.
                                    \nThe values will be used in np.random.uniform(params[0], params[1], fault_length)
                                    \nparams[0] represents the lower bound
                                    \nparams[1] represents the upper bound""")

                change_lst = np.random.uniform(params[0], params[1], self.fault_length)
                self.values[self.start:self.stop] += change_lst
            else:
                raise ValueError('noise_type needs to be \"gaussian\" or \"uniform\" ')
        except ValueError as e:
            print(f"Error: {e}")

    def plot_compare_values(self):
        """
        This method can be used to plot the injected fault and compare it to the original data
        """
        # calculate the middle of the original y values
        y_mid =  (max(self.original_values) - min(self.original_values)) / 2 + min(self.original_values)

        fig, ax = plt.subplots()

        # plot the original values
        ax.plot(self.original_values, color='#1f77b4', label="Original")

        # plot the injected values
        ax.plot(self.values, color='#d62728', label="Fault")

        # plot a horizontal line in the middle of the original values
        ax.hlines(y=y_mid, xmin=0, xmax=len(self.values), color="black")

        #plot a vertical line where the fault starts
        ax.vlines(
            x=self.start,
            ymin=min(0, min(self.values)),
            ymax=max(1, max(self.values)*2),
            color="red",
        )
        #plot a vertical line where the fault ends
        ax.vlines(
            x=self.stop,
            ymin=min(0, min(self.values)),
            ymax=max(1, max(self.values)*2),
            color="red",
        )

        ax.set(xlabel="time", ylabel="value")

        # dynamically change the y limits based on the values
        ax.set_ylim([min(min(self.original_values), min(self.values)) * 0.995, max(max(self.original_values), max(self.values)) * 1.005])
        ax.grid()
        plt.legend()
        plt.show()

