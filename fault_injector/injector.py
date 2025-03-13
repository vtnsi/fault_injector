import random
import matplotlib.pyplot as plt
import numpy as np

class FaultInjection:
    def __init__(self, values, start=None, stop=None, increasing=0):
        """
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
        # this will revert values back to the original state
        self.values = self.original_values.copy()

    def inject_fault(self, change_lst):
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
        # list of NaN values
        change_lst = [np.nan] * self.fault_length

        self.values[self.start:self.stop] = change_lst


    def inject_stuck_value(self, stuck_val=None):
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
        if params is None:
            params = []
        try:
            if not isinstance(params, list):
                raise ValueError("params needs to be a list")
            elif noise_type == 'gaussian':
                if len(params) == 0:
                    # calculate mean
                    params.append(np.array(self.values[self.start:self.stop]).mean())
                    # calculate standard deviation
                    params.append(np.std(self.values[self.start:self.stop]))
                elif len(params) > 2 or len(params) == 1:
                    raise ValueError("""Params should either be an empty list or it should contain 2 elements.
                                    \nThe values will be used in np.random.normal(params[0], params[1], fault_length)
                                    \nparams[0] typically represents the mean of the distribution
                                    \nparams[1] typically represents the standard deviation""")

                change_lst = np.random.normal(params[0], params[1], self.fault_length)
                self.values[self.start:self.stop] = change_lst

            elif noise_type == 'uniform':
                if len(params) == 0:
                    # calculate min value
                    params.append(0.999 * self.original_average)
                    # calculate max value
                    params.append(1.001 * self.original_average)
                elif len(params) > 2 or len(params) == 1:
                    raise ValueError("""Params should either be an empty list or it should contain 2 elements.
                                    \nThe values will be used in np.random.uniform(params[0], params[1], fault_length)
                                    \nparams[0] represents the lower bound
                                    \nparams[1] represents the upper bound""")

                change_lst = np.random.uniform(params[0], params[1], self.fault_length)
                self.values[self.start:self.stop] = change_lst
            else:
                raise ValueError('noise_type needs to be \"gaussian\" or \"uniform\" ')
        except ValueError as e:
            print(f"Error: {e}")

    def plot_compare_values(self):
        # this function can be used to plot the injected fault and compar it to the original data
        # calculate the middle of the original y values
        y_mid =  (max(self.original_values) - min(self.original_values)) / 2 + min(self.original_values)

        fig, ax = plt.subplots()
        # plot the injected values
        ax.plot(self.values, color="blue")

        # plot the original values
        ax.plot(self.original_values, color="blue", alpha=0.2)

        # plot a horizontal line in the middle of the original values
        ax.hlines(y=0.50, xmin=0, xmax=len(self.values), color="black")

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

        plt.show()

