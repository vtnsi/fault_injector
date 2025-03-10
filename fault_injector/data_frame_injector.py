import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import fault_injector.injector as injector

'''
To Do:
- convert to proper class formatting
- add comments/descriptions
- add error handling for the class
- update demo
- update documentation (ReadME)
'''

class DataFrameFaultInjection():
    def __init__(self, df:pd.DataFrame, column_names, start_val:int, stop_val:int):
        """
        DataFrameFaultInjection is an extension of the FaultInjection class that allows
            users to inject faults into multiple columns in a dataframe

        Args:
            df (pd.DataFrame): Pandas DataFrame
            column_names (list or string): represents either a single column name or a 
                list of column names in df that will be injected with the fault
            start_val (int): int value representing the starting index value for the fault
            stop_val (int): int value representing the last index value for the fault
        """       
        self.fault_dict = {}
        self.original_df = df.copy()
        self.fault_df = df.copy()

        if isinstance(column_names, str):
            column_names = [column_names]
        self.column_names = column_names
        self.start_val = start_val
        self.stop_val = stop_val

    def inject_fault(self):
        """
        This function creates a dictionary of FaultInjection class objects and stores 
            them in self.fault_dict. This allows the user to utilize all of the FaultInjection
            capabilities for their desired columns.

        Returns:
            self.fault_dict (dict): this dictionary of FaultInjection class objects, 
                where the keys represent the column names
        """        
        for i in self.column_names:
            original_lst = list(self.original_df[i].values)
            df_inject = injector.FaultInjection(values=original_lst, start=self.start_val, stop=self.stop_val, increasing=1)
            
            self.fault_dict[i] = df_inject
        return self.fault_dict

    def update_df(self):
        """
        This function returns an updated df that now contains the faulty data

        Returns:
            self.fault_df (pd.DataFrame): this dataframe takes the same format of the original 
                data. The columns that were injected with faults are now updated with the fault data
        """        
        for key in self.fault_dict.keys():
            self.fault_df[key] = self.fault_dict[key].values

        return self.fault_df