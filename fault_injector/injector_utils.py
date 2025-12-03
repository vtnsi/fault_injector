import random
import matplotlib.pyplot as plt
import numpy as np

class InjectorUtils:
    def __init__(self, values, start=None, stop=None, increasing=0):
        r"""
        The GenericFault class is designed to take in a list of numeric values and inject a fault into the values

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
            raise ValueError(f"Initialization error: {e}")


    def restore_values(self):
        r"""
        This will revert values back to the original state
        """

        self.values = self.original_values.copy()


    def inject_fault(self, change_lst:list, replace_values:bool = False):
        """This is a generic method that can be used to add custom faults to the original values.
        It takes in a list of numeric values that will be added to the existing values.
        For example, this method is used by the `inject_drift` method to add the drift values to the existing values.

        Note: this method is used to add values to the existing values **not** replace the existing values.

        Args:
            change_lst (list): a list of numeric values

            replace_values (bool): indicates if the change_lst will be added to the original values or replace the original values
        """
        if len(change_lst) != self.stop - self.start:
            raise ValueError(f"change_lst must have length {self.stop - self.start}")

        if replace_values:
            self._replace_fault(change_lst)
        else:
            self._add_fault(change_lst)

        # convert back to a list
        self.values = list(self.values)

    def _add_fault(self, change_lst:list):
        """
        Method designed to add the fault to the existing values over the desired range

        Args:
            change_lst (list): List of numeric values representing the delta of the values caused by the fault
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


    def _replace_fault(self, change_lst:list):
        """
        Replace the values with the new fault values

        Args:
            change_lst (list): list of the new values caused by the fault
        """
        self.values[self.start:self.stop] = change_lst


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