import pandas as pd
import numpy as np
from fault_injector.injector import Injector


class DataFrameInjector:
    """
    Injects DataFrameFault output into specific or all columns of a DataFrame,
    using the existing Injector. Supports horizontal (array-per-row) and vertical
    (scalar) columns. Supports optional column mapping.
    """

    def __init__(self, df: pd.DataFrame):
        self.original_df = df.copy()
        self.df = df.copy()
        self.horizontal = self._is_horizontal(self.original_df)


    @staticmethod
    def _is_horizontal(df: pd.DataFrame) -> bool:
        """
        Horizontal DF: every element in the df is a list/array.
        Vertical DF: normal numbers.
        """
        for col in df.columns:
            for val in df[col].values:
                if not (isinstance(val, (list, np.ndarray))):
                    return False
        return True

    @staticmethod
    def _assert_same_orientation(df_a, df_b, name_a="original_df", name_b="faulty_df"):
        """
        Ensure both dataframes are either horizontal or vertical.
        """
        a_h = DataFrameInjector._is_horizontal(df_a)
        b_h = DataFrameInjector._is_horizontal(df_b)

        if a_h != b_h:
            raise TypeError(
                f"Incompatible orientation: {name_a} is "
                f"{'horizontal' if a_h else 'vertical'} but {name_b} is "
                f"{'horizontal' if b_h else 'vertical'}"
            )

    def inject_faults(
        self,
        faulty_df: pd.DataFrame,
        columns_to_inject: list = None,
        column_map: dict = None,
        start: int = None,
        stop: int = None,
        replace: bool = True,
    ):
        """
        Inject faulted values into the DataFrame.

        Parameters
        ----------
        faulty_df : pd.DataFrame
            Output of DataFrameFault.
        columns_to_inject : list[str], optional
            Columns in the original DF to inject. If None -> use ALL columns.
        column_map : dict, optional
            Mapping { original_col : faulty_df_col }.
            If None -> assume identical names.
        start, stop : int
            Row range (original DF index) where injection occurs.
        replace : bool
            True -> replace values, False -> add deltas.
        """
        # Orientation check
        self._assert_same_orientation(self.original_df, faulty_df)
        horizontal = self.horizontal

        # Determine range
        n = len(self.df)
        start = 0 if start is None else start
        stop = n if stop is None else stop

        if not (0 <= start <= stop <= n):
            raise ValueError("Invalid start/stop range.")

        inject_len = stop - start

        # Columns to inject
        if columns_to_inject is None:
            columns_to_inject = list(self.df.columns)

        # Column mapping
        if column_map is None:
            column_map = {col: col for col in columns_to_inject}
        else:
            # ensure mapping exists
            column_map = {col: column_map.get(col, col) for col in columns_to_inject}

        # Validate columns
        for orig_col, fault_col in column_map.items():
            if orig_col not in self.df.columns:
                raise KeyError(f"Original DataFrame missing column {orig_col}")
            if fault_col not in faulty_df.columns:
                raise KeyError(f"Fault DataFrame missing column {fault_col}")

        # Main injection loop
        for orig_col, fault_col in column_map.items():

            faulty_vals = faulty_df[fault_col].values
            if len(faulty_vals) != inject_len:
                raise ValueError("Faulty column length mismatch for injection range.")

            if horizontal:
                # HORIZONTAL: each row contains list/array
                for local_i, global_i in enumerate(range(start, stop)):
                    orig_row = self.df.at[global_i, orig_col]
                    fault_row = faulty_vals[local_i]

                    orig_arr = np.array(orig_row, dtype=float)
                    fault_arr = np.array(fault_row, dtype=float)

                    if orig_arr.shape != fault_arr.shape:
                        raise ValueError("Row array shape mismatch.")

                    new_arr = fault_arr if replace else orig_arr + fault_arr
                    self.df.at[global_i, orig_col] = new_arr

            else:
                # VERTICAL: scalar values
                for local_i, global_i in enumerate(range(start, stop)):
                    orig_val = self.df.at[global_i, orig_col]
                    fault_val = faulty_vals[local_i]

                    if replace:
                        new_val = fault_val
                    else:
                        new_val = orig_val + fault_val

                    self.df.at[global_i, orig_col] = new_val

        return self.df

    def restore_original(self):
        """Restore the DataFrame to its original state."""
        self.df = self.original_df.copy()
        return self.df
