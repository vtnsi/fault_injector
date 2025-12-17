# -*- coding: utf-8 -*-
from __future__ import annotations
import copy
from typing import Any, Dict, List, Optional, Sequence, Type, Union
import numpy as np
import fault_injector.fault_lib as _faultlib

ParamValue = Union[int, float, bool, str, Sequence[Any]]
FaultSpec = Union[str, Type, object]
FaultMetadata = Dict[str, Any]


class DfUtils:
    """
    Utility mixin for DataFrameFault.

    Responsibilities:
        - Fault registry (builtin + user)
        - Parameter broadcasting (horizontal/vertical)
        - Fault instantiation
        - Component combination
        - Metadata build / restore
    """

    _builtin_registry: Dict[str, Type] = {}

    def __init__(self, registry: Optional[Dict[str, Type]] = None) -> None:
        """
        Initialize the utility with optional user registry.

        args:
        - registry (Optional[Dict[str, Type]]): User-supplied fault registry

        """
        self._init_registry(registry)


    @classmethod
    def _build_builtin_registry(cls) -> None:
        """
        Populate the builtin fault registry from the fault library.
        """
        if cls._builtin_registry:
            return
        for name in getattr(_faultlib, "__all__", []):
            if name == "utils":
                continue
            obj = getattr(_faultlib, name, None)
            if isinstance(obj, type):
                cls._builtin_registry[name.lower()] = obj

    def _init_registry(self, user_registry: Optional[Dict[str, Type]] = None) -> None:
        """
        Initialize the effective fault registry combining builtin and user registry.

        args:
        - user_registry (Optional[Dict[str, Type]]): User-supplied fault registry

        """
        self._build_builtin_registry()
        self.registry: Dict[str, Type] = dict(self._builtin_registry)
        if user_registry:
            for k, v in user_registry.items():
                self.registry[k.lower()] = v

    def register_fault(self, name: str, cls: Type) -> None:
        """
        Register a new fault class in the registry.

        args:
        - name (str): Name of the fault
        - cls (Type): Fault class to register

        """
        self.registry[name.lower()] = cls

    def _lookup_fault_class(self, name: str) -> Type:
        """
        Retrieve a fault class by name from the registry.

        args:
        - name (str): Name of the fault

        outputs:
        - cls (Type): Fault class associated with the name
        """
        cls = self.registry.get(name.lower())
        if cls is None:
            raise KeyError(f"Fault class '{name}' not found in registry.")
        return cls


    @staticmethod
    def _is_scalar_param(v: Any) -> bool:
        """
        Determine if a fault parameter is scalar (not an array, list, or callable).

        args:
        - v (Any): Parameter value to check

        outputs:
        - is_scalar (bool): True if val is scalar, False otherwise
        """
        return not isinstance(v, (list, tuple, np.ndarray))

    def _resolve_param(
        self,
        param: ParamValue,
        df_length: int,
        row_idx: Optional[int] = None,
        horizontal: bool = True,
        repeat: bool = False,
    ) -> Any:
        """
        Resolve a fault parameter for a specific row/column context.

        args:
        - param (Any): The parameter value to resolve (scalar, list, or callable)
        - df_length (int): Total number of rows in the DataFrame
        - row_idx (Optional[int]): Row index for horizontal generation
        - horizontal (bool): Whether generation is horizontal
        - repeat (bool): Whether parameter values should repeat when exhausted

        outputs:
        - resolved_value (Any): The resolved parameter value for this context
        """
        if self._is_scalar_param(param):
            return param

        seq = list(param)
        L = len(seq)
        if L == 0:
            raise ValueError("Parameter list must have length >= 1")
        if L == 1:
            return seq[0]

        if L > df_length:
            raise ValueError(f"Parameter list length {L} greater than df_length {df_length}")

        if L == df_length:
            if horizontal:
                if row_idx is None:
                    raise ValueError("row_idx must be provided for horizontal resolution")
                return seq[row_idx]
            else:
                raise ValueError("Per-row parameter lists not allowed in vertical mode. Use scalar or repeatable shorter list.")

        # L < df_length
        if repeat:
            if horizontal and row_idx is not None and row_idx < L:
                return seq[row_idx]
            return seq[-1]
        else:
            raise ValueError(f"Parameter list length {L} smaller than df_length {df_length} and repeat=False")


    def _instantiate_fault(self, fault_spec: FaultSpec, params: Optional[Dict[str, Any]] = None):
        """
        Instantiate a fault object with the given parameters.

        args:
        - fault_class (type): Fault class to instantiate
        - params (Dict[str, Any]): Parameters to pass to the fault constructor

        outputs:
        - fault_obj (Any): Instantiated fault object
        """
        params = params or {}
        if not isinstance(fault_spec, (str, type)):
            return copy.deepcopy(fault_spec)
        cls = fault_spec if isinstance(fault_spec, type) else self._lookup_fault_class(fault_spec)
        try:
            return cls(**params) if params else cls()
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate fault {fault_spec} with {params}: {e}")


    @staticmethod
    def _combine_components_for_row(components: List[np.ndarray], mode: Optional[str] = None) -> np.ndarray:
        """
        Combine multiple fault components for a single row.

        args:
        - components (List[np.ndarray]): List of component arrays to combine
        - mode (Optional[str]): Combination mode (e.g., sum, mean, or custom)

        outputs:
        - combined (np.ndarray): Combined array for this row
        """
        if not components:
            raise ValueError("No components to combine.")
        arrs = [np.asarray(a) for a in components]
        if any(a.shape != arrs[0].shape for a in arrs):
            raise ValueError("All component arrays must have the same shape.")
        stacked = np.vstack(arrs)
        mode = (mode or "sum").lower()
        if mode in ("sum", "add"):
            return np.sum(stacked, axis=0)
        if mode in ("mean", "avg", "average"):
            return np.mean(stacked, axis=0)
        raise ValueError(f"Unknown combine mode: {mode}")


    def _build_metadata(self) -> FaultMetadata:
        """
        Build metadata describing assigned faults and generation settings.

        outputs:
        - metadata (Dict[str, Any]): Dictionary containing configuration and fault assignment details
        """
        meta = {
            "col_names": getattr(self, "col_names", []),
            "horizontal": getattr(self, "horizontal", False),
            "fault_length": getattr(self, "fault_length", None),
            "df_length": getattr(self, "df_length", None),
            "repeat": getattr(self, "repeat", True),
            "multi_fault": getattr(self, "multi_fault", False),
            "combine_mode": getattr(self, "combine_mode", None),
            "include_individual_faults": getattr(self, "include_individual_faults", False),
            "custom_fault": getattr(self, "custom_fault", False),
            "faults": {},
        }
        for col, assigns in getattr(self, "faults", {}).items():
            meta["faults"][col] = [
                {
                    "fault_type": a.get("fault_type") if isinstance(a.get("fault_type"), str)
                    else type(a.get("fault_type")).__name__,
                    "params": a.get("params"),
                    "fault_length": a.get("fault_length"),
                    "repeat": a.get("repeat"),
                }
                for a in assigns
            ]
        return meta

    @classmethod
    def from_metadata(cls, metadata: FaultMetadata) -> "DfUtils":
        """
        Restore a DfUtils instance from metadata.

        args:
        - metadata (FaultMetadata): Dictionary containing fault assignments and settings

        outputs:
        - inst (DfUtils): Restored instance
        """
        inst = cls(registry=None)
        for key in ["col_names", "horizontal", "fault_length", "df_length",
                    "repeat", "multi_fault", "combine_mode",
                    "include_individual_faults", "custom_fault"]:
            setattr(inst, key, metadata.get(key))
        inst.faults = {}
        for col, assigns in metadata.get("faults", {}).items():
            inst.faults[col] = [
                {"fault_type": a.get("fault_type"),
                 "params": a.get("params"),
                 "fault_obj": None,
                 "fault_length": a.get("fault_length"),
                 "repeat": a.get("repeat", inst.repeat)}
                for a in assigns
            ]
        return inst


    def _validate_init_args(self) -> None:
        """
        Validate initialization arguments.

        """
        if not isinstance(getattr(self, "col_names", []), (list, tuple)):
            raise ValueError("col_names must be a list or tuple of strings.")

    @staticmethod
    def _warn(msg: str) -> None:
        """
        Print a warning message.

        args:
        - msg (str): Warning message to print

        """
        print(f"Warning: {msg}")
