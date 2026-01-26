Installation
============

This guide explains how to install **Fault Injector**, a Python package for simulating
faults in time-series or sensor data.

Requirements
------------
- Python ≥ 3.8
- NumPy
- Matplotlib
- Pandas

Install via GitHub
------------------
Until then, install directly from the GitHub repository:

.. code-block:: bash

    pip install git+https://github.com/vtnsi/fault_injector.git

Install from source
-------------------

Alternatively, you can clone the repository manually and install it in editable mode:

.. code-block:: bash

    git clone https://github.com/vtnsi/fault_injector.git
    cd fault_injector
    pip install -e .

Verifying installation
----------------------

To check that the package is installed correctly:

.. code-block:: bash

    python -c "from fault_injector import FaultInjection; print('Fault Injector imported successfully!')"

Importing
---------

.. code-block:: python

    from fault_injector.fault_lib import *
    import fault_injector.injector as injector
    import fault_injector.df_injector as df_injector
