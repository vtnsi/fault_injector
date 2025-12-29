Offset Fault
============

Define Fault
------------

An **offset fault** models a sensor error where a constant bias is added
to the measured values during a specific time window. Unlike drift,
which accumulates over time, offset is a fixed deviation applied
instantly when the fault occurs.

Offset faults commonly arise from calibration errors, sudden
environmental changes, or sensor misalignment.

The **offset value** can be defined relative to the signal as:

.. math::

   \text{offset\_value} = \text{mean}(x_s, x_{s+1}, \ldots, x_{e-1}) \cdot \text{offset\_rate}

where ``offset_rate`` is a scaling factor.

Math Behind Fault
-----------------

Assume a univariate time series of true sensor values:

- **True signal:** :math:`x_i`, for index :math:`i = 0, 1, 2, ..., N-1`
- **Fault start index:** :math:`s`
- **Fault end index:** :math:`e`

Linear Offset Model
-------------------

The observed (faulty) signal :math:`y_i` is defined as:

.. math::

   y_i =
   \begin{cases}
   x_i + \text{offset\_value}, & s \le i < e \\
   x_i, & \text{otherwise}
   \end{cases}

This represents a constant additive bias during the fault window.

Impact on Statistical Properties
--------------------------------

Let the original signal :math:`x_i` have mean and variance:

.. math::

   \mu_x = \mathbb{E}[x_i], \qquad \sigma_x^2 = \mathrm{Var}(x_i)

Assume the offset is applied for indices :math:`i = s, s+1, ..., e-1`,
with fault duration:

.. math::

   n = e - s

Effect on the Mean
------------------

The offset at time :math:`i` is:

.. math::

   \delta_i = \text{offset\_value}

The mean of the faulty signal becomes:

.. math::

   \mu_y = \mu_x + \text{offset\_value}

Thus, offset faults introduce a **systematic shift in the mean** without
changing the underlying signal dynamics.

Effect on the Variance
----------------------

Since the offset is constant, the variance of the faulty signal is:

.. math::

   \sigma_y^2 = \mathrm{Var}(x_i + \delta_i)
              = \mathrm{Var}(x_i)
              = \sigma_x^2

Key Takeaway
------------

Offset faults shift the average signal value while leaving the variance
unchanged.

Example
-------

An example of an offset fault compared to the true values is shown below:

.. image:: ../../images/demos/offset_fault/comparison.png
   :alt: Offset fault example
