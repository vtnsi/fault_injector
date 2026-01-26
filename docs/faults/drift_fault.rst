Drift Fault
===========

Define Fault
------------

A **sensor drift fault** models a gradual, systematic deviation of sensor
readings from their true values over time. Unlike abrupt faults (e.g.,
spikes or dropouts), drift accumulates slowly and can be difficult to
detect without trend analysis.

The drift rate :math:`r \in \mathbb{R}` represents the slope of the fault-induced offset.
Larger magnitudes of :math:`r` produce faster deviation from the true signal,
while :math:`r = 0` implies no drift.


Sensors can naturally drift over time due to aging, temperature
effects, calibration loss, or environmental exposure.

Math Behind Fault
-----------------

Assume a univariate time series of true sensor values:

- **True signal:** :math:`x_i`, for index :math:`i = 0, 1, ..., N-1`
- **Fault start index:** :math:`s`
- **Fault end index:** :math:`e`
- **Drift rate:** :math:`r`

Linear Drift Model
------------------

The observed (faulty) signal :math:`y_i` is defined as:

.. math::

   y_i =
   \begin{cases}
   x_i, & i < s \\
   x_i + (i - s) \cdot r, & s \le i < e \\
   x_i, & i \ge e
   \end{cases}


Key takeaway
------------

Sensor drift affects both the mean and the variance, shifting the average
value while also increasing variability over time.

Example
-------

An example of a drift fault compared to the true values is shown below:

.. image:: ../../images/demos/drift_fault/comparison.png
   :alt: Drift fault example
