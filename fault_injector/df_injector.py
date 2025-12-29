# -*- coding: utf-8 -*-
"""
dataframe fault injector
"""
import numpy as np
import pandas as pd


class DataFrameInjector:
    """
    Class designed to help inject faults into dataframes

    Args:
        injector_dict (dict):
        - keys correspond to column names in df
        - values correspond to fault instances
    """

    def __init__(self, injector_dict:dict):

        self.injector_dict = injector_dict
        self._check_injector_dict()


    def inject_faults(self, df:pd.DataFrame):
        """
        Inject faults into dataframe

        Args:
            df (dataframe): contains numerical datatypes

        Returns:
            dataframe: altered data after injecting faults
        """
        df = df.copy()
        self._check_df_and_injector_dict(df)

        for col, f in self.injector_dict.items():
            df[col] = f.inject_fault(df[col].values)
        return df


    def _check_injector_dict(self):
        """
        Check that the injector_dict is a dictionary and that the values are fault instances

        Raises:
            ValueError: Check that the injector_dict is a dictionary
        """
        if not isinstance(self.injector_dict, dict):
            raise ValueError('injector_dict must be a dictionary')

        for col, f in self.injector_dict.items():
            self._check_fault_instance(f, col)


    def _check_df_and_injector_dict(self, df):
        """
        Check that:
        - the injector dict keys are in df
        - the injector values are fault instances
        - df column datatypes

        Args:
            df (dataframe): variable provided in inject_faults

        Raises:
            TypeError: injector_dict key is not in df
        """
        for key, fault in self.injector_dict.items():
            if not key in df.columns:
                raise TypeError(f"injector_dict Key '{key}' is NOT present in df columns.")

            # check that the fault is an instance
            self._check_fault_instance(fault, key)

            # check df[key].values
            self._check_data_type(x=df[key].values, key=key)

    def _check_fault_instance(self, fault, col):
        """
        Check that fault is a fault class instance

        Args:
            fault: f variable in injector_dict

        Raises:
            TypeError: f needs to be a fault instance
        """
        if isinstance(fault, type):
            raise TypeError(f"Error for injector_dict key'{col}' fault: Expected a fault instance \n For example: fault=MyFaultClass(params)")


    def _check_data_type(self, x:np.array, key:str):
        """
        Check that x is an array containing numeric values

        Args:
            x (np.ndarray): array containing numeric values that represent the original value

        Raises:
            ValueError: 'x' must be an array
            ValueError: 'x' must contain numeric values

        """

        if not isinstance(x, np.ndarray):
            raise ValueError(f"Invalid df['{key}'].values type: \n must be an np.ndarray")
        elif not np.issubdtype(x.dtype, np.number):
            raise ValueError(f"Invalid df['{key}']: \n must contain numeric values")