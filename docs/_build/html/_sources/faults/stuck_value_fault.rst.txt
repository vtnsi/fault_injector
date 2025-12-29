Stuck Value Fault
=================

Define Fault
------------

A **stuck value fault** models a sensor error where readings become
constant for a period of time, effectively "freezing" the output at a
fixed value. Unlike offset faults, which add a fixed bias, stuck value
faults replace the sensor signal entirely with a constant.

Stuck value faults can occur due to hardware malfunctions, software
errors, or saturated sensor outputs. The constant value can be chosen
explicitly or generated relative to the underlying signal.

For example, the stuck value can be:

.. math::

   c = \text{mean}(x_s, x_{s+1}, \ldots, x_{e-1}) + d \cdot U(0.01, 0.1) \cdot \text{mean}(x_s, \ldots, x_{e-1})

where :math:`d` is a user-defined scale factor and :math:`U(0.01, 0.1)` is a
random uniform variable.

Math Behind Fault
-----------------

Assume a univariate time series of true sensor values:

- **True signal:** :math:`x_i`, for index :math:`i = 0, 1, 2, \ldots, N-1`
- **Fault start index:** :math:`s`
- **Fault end index:** :math:`e`

Linear Stuck Value Model
------------------------

The observed (faulty) signal :math:`y_i` is defined as:

.. math::

   y_i =
   \begin{cases}
   c, & s \le i < e \\
   x_i, & \text{otherwise}
   \end{cases}

This represents the sensor output being fixed at :math:`c` during the
fault window.

Impact on Statistical Properties
--------------------------------

Let the original signal :math:`x_i` have mean and variance:

.. math::

   \mu_x = \mathbb{E}[x_i], \qquad \sigma_x^2 = \mathrm{Var}(x_i)

Assume the stuck value is applied for indices :math:`i = s, s+1, \ldots, e-1`,
with fault duration:

.. math::

   n = e - s

Effect on the Mean
------------------

The offset at time :math:`i` is:

.. math::

   \delta_i = c - x_i

The mean of the faulty signal becomes:

.. math::

   \mu_y = \frac{1}{N} \left( \sum_{i \notin [s, e)} x_i + \sum_{i \in [s, e)} c \right)
         = \frac{1}{N} \left( \sum_{i \notin [s, e)} x_i + n \cdot c \right)

This shows that stuck value faults **shift the mean toward the stuck
value**, with the effect proportional to the fault duration.

Effect on the Variance
----------------------

The variance of the faulty signal is:

.. math::

   \sigma_y^2 = \frac{1}{N} \sum_{i=0}^{N-1} (y_i - \mu_y)^2

During the fault window, the contribution of the constant values
reduces variability. Therefore, stuck value faults generally **reduce
the variance** compared to the true signal, especially for long fault
durations.

Key Takeaway
------------

Stuck value faults freeze sensor outputs, shifting the mean toward the
stuck value and typically reducing variance.

Example
-------

An example of a stuck value fault compared to the true values is shown below:

.. image:: ../../images/demos/stuck_value_fault/comparison.png
   :alt: Stuck value fault example
