import random
import matplotlib.pyplot as plt
import numpy as np


class DataGen:
    """
    The DataGen class is designed to generate synthetic signal data

    Args:
        rand_max: should be positive, numeric values. Defaults to None.
        rand_min: should be positive, numeric values. Defaults to None.
        size: should be a positive integer. Defaults to 0.
    """

    def __init__(self, rand_max=None, rand_min=None, size=0):
        try:
            if not rand_max is None and not rand_min is None:
                self._validate_range(min_val=rand_min, max_val=rand_max, name='random_max and rand_min')
            self.rand_max = rand_max
            self.rand_min = rand_min

            # size will dictate the length of the list.
            if isinstance(size, int) and size > 0:
                self.size = size
            else:
                raise ValueError("Invalid Input (size): \n Value must be a positive int")

        except ValueError as e:
            raise ValueError(f"Initialization error: {e}")

        # values starts as an empty list but over time the randomly generated values will be added to it
        self.values = []


    def random_gen(self) -> np.ndarray:
        """
        The random_gen function will populate self.values with the randomly generated values. To visualize this data, see `plot_values` method.

        Returns:
            np.ndarray: this is the array of generated values
        """
        new_vals = np.random.uniform(self.rand_min, self.rand_max, self.size)
        self.values.extend(new_vals)
        return new_vals


    def frequency_gen(self,
                      amp_params:    dict = None,
                      freq_params:   dict = None,
                      phase_params:  dict = None) -> dict:
        """
        Generate amplitude, frequency, and phase data. To visualize this data, see `plot_frequencies` method.

        Args:
            amp_params      (dict, optional): a dictionary containing the `min` and `max` keys. These params will be used to determine the minimum and maximum amplitude values. If set to None, defaults to dict(min = 0.1, max = 1.0).
            freq_params     (dict, optional): a dictionary containing the `min` and `max` keys. These params will be used to determine the minimum and maximum frequency values. If set to None, defaults to dict(min = 1.0, max = 100.0).
            phase_params    (dict, optional): a dictionary containing the `min` and `max` keys. These params will be used to determine the minimum and maximum phase values. If set to None, defaults to dict(min = 0.0, max = 2 * np.pi).

        Returns:
            dict: a dictionary containing the `amplitudes`, `frequencies`, and `phases` data that makes up the frequency domain.
        """
        base_amp_params = dict(min = 0.1, max = 1.0)
        base_freq_params = dict(min = 1.0, max = 100.0)
        base_phase_params = dict(min = 0.0, max = 2 * np.pi)

        self.amp_params = self._check_and_set_params_dict(amp_params, base_amp_params, "Amplitude")
        self.freq_params = self._check_and_set_params_dict(freq_params, base_freq_params, "Frequency")
        self.phase_params = self._check_and_set_params_dict(phase_params, base_phase_params, "Phase")

        frequency_dict = dict(
            amplitudes = np.random.uniform(self.amp_params['min'], self.amp_params['max'], self.size),
            frequencies = np.random.uniform(self.freq_params['min'], self.freq_params['max'], self.size),
            phases = np.random.uniform(self.phase_params['min'], self.phase_params['max'], self.size),
        )
        return frequency_dict


    def signal_gen(self, params:dict) -> np.ndarray:
        """
        Generate a signal in the time domain. To plot this data, see `plot_signal` method.

        Args:
            params (dict): dictionary containing the `amplitudes`, `frequencies`, and `phases` keys. These keys are all set to numeric lists/arrays. The `frequency_gen` method can be used to generate the frequency domain data

        Raises:
            ValueError: `amplitudes`, `frequencies`, and `phases` arrays must have equal length

        Returns:
            np.ndarray: array of numeric values that corresponds to the time domain signal data
        """
        amplitudes = np.atleast_1d(params['amplitudes'])
        frequencies = np.atleast_1d(params['frequencies'])
        phases = params['phases']
        n = len(params['amplitudes'])
        time = np.arange(n)

        if phases is None:
            phases = np.zeros(n)
        else:
            phases = np.atleast_1d(phases)
            if len(phases) != n:
                raise ValueError("phases must have the same length as amplitudes/frequencies")

        if n > 1:
            t = time[:, None]
            A = amplitudes[None, :]
            F = frequencies[None, :]
            PHI = phases[None, :]
            values = np.sum(A * np.sin(2 * np.pi * F * t / self.size + PHI), axis=1)
        else:
            # Single component: simple, low-memory calculation
            values = amplitudes[0] * np.sin(2 * np.pi * frequencies[0] * time / self.size + phases[0])

        self.values = values
        return values


    def plot_values(self):
        """
        this function can be used to plot the randomly generated data. To generate this data, see `random_gen` method.
        """
        max_val = max(self.values)
        min_val = min(self.values)

        # calculate the middle of the extremes
        y_mid =  (max_val - min_val) / 2 + min_val

        # set the y_max to 2 times the mid. This center the data points on the y axis
        y_max = y_mid * 2

        fig, ax = plt.subplots()
        # plot the generated data
        ax.plot(self.values, color="blue")

        # plot a horizontal line across the middle
        ax.hlines(y=y_mid, xmin=0, xmax=self.size, color="red")

        ax.set(xlabel="time", ylabel="value")

        # ylim assumes the values are positive
        ax.set_ylim([0, y_max])
        ax.grid()

        plt.show()


    def plot_frequencies(self, params:dict, title: str = "Frequency Domain Components", show_phases: bool = True):
        """
        Plot amplitudes vs frequencies, optionally with a phases subplot.
        Frequencies on x-axis. Amplitude stems show magnitude.

        To generate this data, see `frequency_gen` method.
        """

        # Validate that data exists
        if params['amplitudes'] is None or params['frequencies'] is None:
            raise ValueError("You must generate amplitudes and frequencies before plotting.")

        if show_phases and params['phases'] is None:
            raise ValueError("Phases have not been generated. Disable show_phases or call generate_phases().")

        # Configure figure
        if show_phases:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), height_ratios=[2, 1])
        else:
            fig, ax1 = plt.subplots(1, 1, figsize=(10, 4))

        fig.suptitle(title, fontsize=14)

        # Amplitudes vs Frequency
        markerline, stemlines, baseline = ax1.stem(params['frequencies'], params['amplitudes'])
        ax1.set_xlabel("Frequency (Hz)")
        ax1.set_ylabel("Amplitude")
        ax1.grid(True)

        # Phases subplot
        if show_phases:
            markerline2, stemlines2, baseline2 = ax2.stem(params['frequencies'], params['phases'])
            ax2.set_xlabel("Frequency (Hz)")
            ax2.set_ylabel("Phase (rad)")
            ax2.grid(True)

        plt.tight_layout()
        plt.show()


    def plot_signal(self):
        """
        this function can be used to plot the randomly generated signal data

        To generate this data, see `signal_gen` method.
        """
        max_val = max(self.values)
        min_val = min(self.values)

        # calculate the middle of the extremes
        y_mid =  (max_val - min_val) / 2 + min_val

        y_max = max_val * 1.1

        fig, ax = plt.subplots()
        # plot the generated data
        ax.plot(self.values, color="blue")

        # plot a horizontal line across the middle
        ax.hlines(y=y_mid, xmin=0, xmax=self.size, color="red")

        ax.set(xlabel="time", ylabel="value")

        # ylim assumes the values are positive
        ax.set_ylim([min_val, y_max])
        ax.grid()

        plt.show()


    def _validate_range(self, min_val, max_val, name: str):
        if not isinstance(min_val, (int, float)) or not isinstance(max_val, (int, float)):
            raise ValueError(f"{name} range values must be numeric")
        if min_val >= max_val:
            raise ValueError(f"{name} min must be less than {name} max")


    def _validate_range(self, min_val, max_val, name: str):
        if not isinstance(min_val, (int, float)) or not isinstance(max_val, (int, float)):
            raise ValueError(f"{name} range values must be numeric")
        if min_val >= max_val:
            raise ValueError(f"{name} min must be less than {name} max")


    def _check_and_set_params_dict(self, params:dict, base_params:dict, name:str):
        if params is None:
            params = base_params
        for key in base_params.keys():
            if params.get(key) is None:
                params[key] = base_params[key]

        self._validate_range(params['min'], params['max'], name)
        return params