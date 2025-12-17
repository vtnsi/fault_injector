# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union
import copy
import numpy as np
import pandas as pd
from fault_injector.dataframe_fault_utils import DfUtils, FaultSpec
import fault_injector.fault_lib as fault_lib


class DataFrameFault(DfUtils):
    """
    DataFrameFault orchestrates creating fault values per column.

    This class supports:
    - Assigning one or more faults per column
    - Horizontal (row-wise) or vertical (column-wise) fault generation
    - Persistence of fault objects for stateful faults
    - Multi-fault combinations per column

    args:
    - col_names (List[str]): List of column names to assign faults to
    - horizontal (bool): If True, generate faults horizontally (row-wise)
    - fault_length (Optional[int]): Default length of fault sequences
    - df_length (Optional[int]): Number of rows in generated DataFrame
    - repeat (bool): Default for whether fault parameters repeat
    - multi_fault (bool): Allow multiple faults per column
    - combine_mode (Optional[str]): Method to combine multiple faults
    - include_individual_faults (bool): Include extended individual fault components
    - registry (Optional[Dict[str, type]]): Optional registry of fault classes
    - custom_fault (bool): Flag for custom user-defined faults
    - metadata (Optional[Dict[str, Any]]): Optional metadata for initialization
    - persist_state (bool): Persist fault object state across generate_faults calls

    """

    def __init__(
        self,
        col_names: List[str],
        horizontal: bool = False,
        fault_length: Optional[int] = None,
        df_length: Optional[int] = None,
        repeat: bool = True,
        multi_fault: bool = False,
        combine_mode: Optional[str] = None,
        include_individual_faults: bool = False,
        registry: Optional[Dict[str, type]] = None,
        custom_fault: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
        persist_state: bool = False,
    ):
        super().__init__(registry=registry)
        # Primary config
        self.col_names = list(col_names)
        self.horizontal = bool(horizontal)
        self.fault_length = int(fault_length) if fault_length is not None else None
        self.df_length = int(df_length) if df_length is not None else None
        self.repeat = bool(repeat)
        self.multi_fault = bool(multi_fault)
        self.combine_mode = combine_mode
        self.include_individual_faults = bool(include_individual_faults)
        self.custom_fault = bool(custom_fault)
        self.metadata = metadata or {}
        self.persist_state = persist_state

        # Default empty assignment slot per column
        self.faults: Dict[str, List[Dict[str, Any]]] = {
            c: [{
                "fault_type": None,
                "params": None,
                "fault_obj": None,
                "fault_length": None,
                "repeat": self.repeat,
                "persist_state": None
            }]
            for c in self.col_names
        }

        self.df_final: Optional[pd.DataFrame] = None
        self.df_extended: Optional[pd.DataFrame] = None

        self._validate_init_args()

    def assign_fault(
        self,
        col: Union[str, List[str]],
        fault_type: Optional[FaultSpec] = None,
        params: Optional[Dict[str, Any]] = None,
        fault_length: Optional[int] = None,
        repeat: Optional[bool] = None,
        persist_state: Optional[bool] = None,
    ) -> None:
        """
        Assign a fault to a column or list of columns.

        args:
        - col (str | List[str]): Column name(s) to assign fault
        - fault_type (Optional[FaultSpec]): Fault class to apply
        - params (Optional[Dict[str, Any]]): Parameters for the fault
        - fault_length (Optional[int]): Override default fault sequence length
        - repeat (Optional[bool]): Override default repeat behavior
        - persist_state (Optional[bool]): Override default persistence

        """
        cols = [col] if isinstance(col, str) else list(col)
        for c in cols:
            if c not in self.faults:
                self.faults[c] = [{"fault_type": None, "params": None, "fault_obj": None,
                                   "fault_length": None, "repeat": self.repeat, "persist_state": None}]
                self.col_names.append(c)
            entry = {
                "fault_type": fault_type,
                "params": copy.deepcopy(params) if params else None,
                "fault_obj": None,
                "fault_length": int(fault_length) if fault_length is not None else None,
                "repeat": self.repeat if repeat is None else bool(repeat),
                "persist_state": persist_state if persist_state is not None else None,
            }
            if not self.multi_fault:
                self.faults[c] = [entry]
            else:
                self.faults[c].append(entry)

    def generate_faults(self) -> Tuple[pd.DataFrame, Optional[pd.DataFrame], Dict[str, Any]]:
        """
        Generate the faulted DataFrame(s) according to assigned faults.

        outputs:
        - df_final (pd.DataFrame): DataFrame containing the combined fault values
        - df_extended (Optional[pd.DataFrame]): Optional DataFrame of individual fault components
        - metadata (Dict[str, Any]): Metadata describing generated faults

        """
        if not any(a.get("fault_type") for assigns in self.faults.values() for a in assigns):
            raise ValueError("No faults assigned. Assign at least one fault before generating.")

        # Reset non-persistent fault instances
        for assigns in self.faults.values():
            for a in assigns:
                persist = self.persist_state if a.get("persist_state") is None else a["persist_state"]
                if not persist:
                    a["fault_obj"] = None

        if self.horizontal:
            self._generate_faults(range(self.df_length))
        else:
            self._generate_faults(None)

        self.metadata = self._build_metadata()
        return self.df_extended if self.include_individual_faults else self.df_final

    def __call__(self):
        return self.generate_faults()


    def _instantiate_and_run_fault(
        self, col: str, a: Dict[str, Any], ai: int,
        row_idx: Optional[int], length: Optional[int],
        fault_obj: Optional[Any] = None
    ) -> Tuple[np.ndarray, Any]:
        """
        Instantiate a fault object if needed and generate fault output for a column.

        args:
        - col (str): Column name
        - a (Dict[str, Any]): Fault assignment dictionary
        - ai (int): Index of the fault assignment
        - row_idx (Optional[int]): Row index for horizontal generation
        - length (Optional[int]): Number of values to generate
        - fault_obj (Optional[Any]): Existing fault object to reuse

        outputs:
        - output (np.ndarray): Generated fault values
        - fault_obj (Any): Fault object after generation (possibly updated)
        """

        ft = a.get("fault_type")
        if ft is None:
            return np.array([]), fault_obj

        # Determine effective length
        length = length or self.df_length
        if length is None:
            raise ValueError(f"Invalid fault_length for column {col}")

        # Resolve parameters
        params = a.get("params") or {}
        resolved_params = {
            k: self._resolve_param(v, self.df_length, row_idx, self.horizontal, a.get("repeat", self.repeat))
            for k, v in params.items()
        }
        param_varies = any(not self._is_scalar_param(v) for v in params.values())

        # Reuse fault object if available (stateful accumulation)
        if fault_obj is None:
            fault_obj = self._instantiate_fault(ft, resolved_params)
        elif param_varies:
            for pname, pval in resolved_params.items():
                setattr(fault_obj, pname, pval)

        output = np.asarray(fault_obj(length))

        # Persist object across generate_faults() calls if requested
        persist = self.persist_state if a.get("persist_state") is None else a["persist_state"]
        if persist:
            a["fault_obj"] = fault_obj
        else:
            # For horizontal rows, reuse object within same call for accumulation
            if self.horizontal:
                a["fault_obj"] = fault_obj

        return output, fault_obj


    def _generate_faults(self, row_indices: Optional[range]):
        """
        Internal method to generate faults for all columns across rows.

        args:
        - row_indices (Optional[range]): Range of row indices for horizontal generation.
          If None, generates vertical (column-wise) faults.

        """
        col_outputs: Dict[str, List[np.ndarray]] = {c: [] for c in self.col_names}
        extended_components: Dict[str, Dict[str, List[np.ndarray]]] = {c: {} for c in self.col_names}

        is_horizontal = row_indices is not None
        # single iteration for vertical
        row_indices = row_indices if is_horizontal else [None]

        for row_idx in row_indices:
            for col in self.col_names:
                row_components = []
                assigns = self.faults.get(col, [])
                for ai, a in enumerate(assigns, start=1):
                    fault_obj = a.get("fault_obj")
                    length = a.get("fault_length") or self.fault_length or self.df_length
                    out, fault_obj = self._instantiate_and_run_fault(col, a, ai, row_idx, length, fault_obj)
                    row_components.append(out)

                    # Track extended components
                    comp_name = f"{col}_{type(a['fault_type']).__name__}_{ai}" if a['fault_type'] else f"{col}_None_{ai}"
                    extended_components[col].setdefault(comp_name, []).append(out)

                # Combine components for this row
                non_empty = [c for c in row_components if c.size > 0]
                combined = non_empty[0] if len(non_empty) == 1 else \
                    self._combine_components_for_row(non_empty, self.combine_mode) if non_empty else np.array([])

                col_outputs[col].append(combined)

        # Build final dataframes
        if is_horizontal:
            self.df_final = pd.DataFrame({col: pd.Series(vals, dtype=object) for col, vals in col_outputs.items()})
            if self.include_individual_faults:
                ext_cols = {name: pd.Series(lst, dtype=object)
                            for col, comps in extended_components.items()
                            for name, lst in comps.items()}
                self.df_extended = pd.DataFrame(ext_cols) if ext_cols else None
            else:
                self.df_extended = None
        else:
            # vertical: use single combined output per column
            df_dict = {col: vals[0] for col, vals in col_outputs.items()}
            self.df_final = pd.DataFrame(df_dict)
            if self.include_individual_faults:
                self.df_extended = pd.DataFrame({name: vals[0] for col, comps in extended_components.items() for name, vals in comps.items()})
            else:
                self.df_extended = None



    #  Metadata
    @classmethod
    def from_metadata(cls, metadata: Dict[str, Any]) -> "DataFrameFault":
        """
        Create a DataFrameFault instance from saved metadata.

        args:
        - metadata (Dict[str, Any]): Metadata previously returned from generate_faults

        outputs:
        - instance (DataFrameFault): Reconstructed instance
        """

        inst = super(DataFrameFault, cls).from_metadata(metadata)
        if not isinstance(inst, cls):
            raise RuntimeError("from_metadata produced instance of unexpected type.")
        return inst
