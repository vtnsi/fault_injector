import random
import matplotlib.pyplot as plt
import numpy as np


class DataGen:

    def __init__(self, rand_max=None, rand_min=None, size=0):
        """
        The DataGen class is designed to generate synthetic signal data

        Args:
            rand_max: should be positive, numeric values. Defaults to None.
            rand_min: should be positive, numeric values. Defaults to None.
            size: should be a positive integer. Defaults to 0.
        """
        try:
            # rand_max & rand_min control the extremes for the generated data
            if isinstance(rand_max, (float, int)):
                self.rand_max = rand_max
            else:
                raise ValueError("Invalid Input (rand_max): \n Value must be an int or a float")

            if isinstance(rand_min, (float, int)) and rand_min < rand_max:
                self.rand_min = rand_min
            else:
                raise ValueError("Invalid Input (rand_min): \n Value must be an int or a float and less than rand_max")

            # size will dictate the length of the list.
            if isinstance(size, int) and size > 0:
                self.size = size
            else:
                raise ValueError("Invalid Input (size): \n Value must be a positive int")
        except ValueError as e:
            raise ValueError(f"Initialization error: {e}")

        # values starts as an empty list but over time the randomly generated values will be added to it
        self.values = []

    def random_gen(self):
        """
        The random_gen function will populate self.values with the randomly generated values
        """
        new_vals = np.random.uniform(self.rand_min, self.rand_max, self.size)
        self.values.extend(new_vals)

    def plot_values(self):
        """
        this function can be used to plot the randomly generated data
        """
        # calculate the middle of the extremes
        y_mid =  (self.rand_max - self.rand_min) / 2 + self.rand_min

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
