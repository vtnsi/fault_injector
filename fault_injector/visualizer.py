# -*- coding: utf-8 -*-
"""
plotting class
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class FaultVisualizer:
    """
    This class is designed to make it easier to plot and compare faulty data to its original data.

    Args:
        font_size (int, optional): controls the fault size in the plots. Defaults to 16.
        plot_size (tuple, optional): controls the plot/fig size. Defaults to (10, 4).
        colors_dict (dict, optional): dictionary that controls the colors used in the plot. Defaults to `original` being blue, `new` being red, and `delta` being purple.
    """
    def __init__(self, font_size:int=16, plot_size=(10, 4), colors_dict:dict=None):
        self.font_size = font_size
        self.plot_size = plot_size


        if colors_dict is None:
            colors_dict = {
                            "original": "blue",
                            "new": "red",
                            "delta": "purple"
                            }
        self.colors = colors_dict

        if self.colors.get('original'):
            self.colors['original'] = 'blue'

        if self.colors.get('new'):
            self.colors['new'] = 'red'

        if self.colors.get('delta'):
            self.colors['delta'] = 'purple'


    def plot_fault_delta(self, original_values:np.ndarray, new_values:np.ndarray, title:str=None, file_name:str=None):
        """
        Plot the fault delta (new - original)

        Args:
            original_values (np.ndarray): array of numeric values used to represent the original/true values
            new_values (np.ndarray): array of numeric values used to represent the fault values
            title (str, optional): used as the title in the plot. Defaults to None.
            file_name (str, optional): file name when saving the figure. When not equal to None, the plot will be saved. Defaults to None.
        """
        self._check_data_type(x=original_values, key='original_values')
        self._check_data_type(x=new_values, key='new_values')

        delta = new_values - original_values

        fig, ax = plt.subplots(figsize=self.plot_size)

        # plot delta
        ax.plot(delta, color=self.colors['delta'], label="Delta")

        # axis labels
        ax.set(xlabel="time", ylabel="delta")

        # set title
        fig.suptitle(title, fontsize=self.font_size)

        ax.grid()
        ax.legend()
        plt.tight_layout()

        # either show or save
        if file_name is None:
            plt.show()
        else:
            plt.savefig(f"{file_name}.png")


    def plot_fault_delta_df(self, original_df:pd.DataFrame, new_df:pd.DataFrame, title:str=None, file_name:str=None):
        """
        Plot all of the columns in the dataframes

        Args:
            original_df (pd.DataFrame): original values
            new_df (pd.DataFrame): new values
            title (str, optional): base of plot titles. Defaults to None.
            file_name (str, optional): base of the file name. Defaults to None.
        """
        self._check_dfs(original_df, new_df)
        for col in original_df.columns:
            if not title is None:
                new_title = f'{title}: {col}'
            else:
                new_title = None

            if not file_name is None:
                new_file_name = f'{file_name}_{col}'
            else:
                new_file_name = None
            self.plot_fault_delta(original_values=original_df[col].values, new_values=new_df[col].values, title=new_title, file_name=new_file_name)



    def plot_comparison(self, original_values:np.ndarray, new_values:np.ndarray, title:str=None, file_name:str=None):
        """
        Plot original values and new values

        Args:
            original_values (np.ndarray): _description_
            new_values (np.ndarray): _description_
            title (str, optional): _description_. Defaults to None.
            file_name (str, optional): _description_. Defaults to None.
        """
        self._check_data_type(x=original_values, key='original_values')
        self._check_data_type(x=new_values, key='new_values')

        fig, ax = plt.subplots(figsize=self.plot_size)

        # plot original (blue)
        ax.plot(original_values, color=self.colors['original'], label="Original")

        # plot new values (red)
        ax.plot(new_values, color=self.colors['new'], label="New Values")

        # axis labels
        ax.set(xlabel="time", ylabel="value")

        # dynamic y-limit
        ymin = min(min(original_values), min(new_values)) * 0.995
        ymax = max(max(original_values), max(new_values)) * 1.005
        ax.set_ylim([ymin, ymax])

        # set title
        fig.suptitle(title, fontsize=self.font_size)

        ax.grid()
        ax.legend()
        plt.tight_layout()

        # either show or save
        if file_name is None:
            plt.show()
        else:
            plt.savefig(f"{file_name}.png")


    def plot_comparison_df(self, original_df:pd.DataFrame, new_df:pd.DataFrame, title:str=None, file_name:str=None):
        """
        Plot all of the columns in the dataframes

        Args:
            original_df (pd.DataFrame): original values
            new_df (pd.DataFrame): new values
            title (str, optional): base of plot titles. Defaults to None.
            file_name (str, optional): base of the file name. Defaults to None.
        """
        self._check_dfs(original_df, new_df)
        for col in original_df.columns:
            if not title is None:
                new_title = f'{title}: {col}'
            else:
                new_title = None

            if not file_name is None:
                new_file_name = f'{file_name}_{col}'
            else:
                new_file_name = None
            self.plot_comparison(original_values=original_df[col].values, new_values=new_df[col].values, title=new_title, file_name=new_file_name)


    def _check_data_type(self, x:np.array, key:str='x'):
        """
        Check that x is an array containing numeric values

        Args:
            x (np.ndarray): array containing numeric values that represent the original value

        Raises:
            ValueError: 'x' must be an array
            ValueError: 'x' must contain numeric values

        """

        if not isinstance(x, np.ndarray):
            raise ValueError(f"Invalid {key}: \n must be an np.ndarray")
        elif not np.issubdtype(x.dtype, np.number):
            raise ValueError(f"Invalid {key}: \n must contain numeric values")


    def _check_dfs(self, original_df, new_df):
        """
        Check that:
        - the new_df keys are in original_df
        - df column datatypes

        Args:
            original_df (dataframe): original values
            new_df (dataframe): new values

        Raises:
            TypeError: new_df key is not in original_df
        """
        for col in original_df.columns:
            if not col in new_df.columns:
                raise TypeError(f"original_df '{col}' is NOT present in new_df columns.")

            # check df[key].values
            self._check_data_type(x=original_df[col].values, key=f'original_df: {col}')
            self._check_data_type(x=new_df[col].values, key=f'new_df: {col}')