import numpy as np
from fault_injector.injector_utils import InjectorUtils

class Injector(InjectorUtils):

    def __init__(self, values, start, stop):
        super().__init__(values, start=start, stop=stop)

    def __call__(self, fault_obj:list, replace_values:bool = False, values=None):
        if values != None:
            self.values = values
        self.inject_fault(change_lst=fault_obj, replace_values=replace_values)