NaN Fault
=========

Define Fault
------------

A **NaN fault** models a sensor failure where readings are completely
missing for a continuous period of time. During the fault window, the
sensor does not report valid numeric values, and measurements are
represented as ``NaN`` (Not a Number).

NaN faults commonly occur due to communication dropouts, power failures,
buffer overflows, or temporary sensor disconnections. Unlike additive
faults (e.g., bias or drift), NaN faults do not alter the underlying
signal values—they remove them entirely from observation.

Math Behind Fault
-----------------

Assume a univariate time series of true sensor values:

- **True signal:** :math:`x_i`, for index :math:`i = 0, 1, ..., N-1`
- **Fault start index:** :math:`s`
- **Fault end index:** :math:`e`

Linear NaN Model
----------------

The observed (faulty) signal :math:`y_i` is defined as:

.. math::

   y_i =
   \begin{cases}
   \text{NaN}, & s \le i < e \\
   x_i, & \text{otherwise}
   \end{cases}

Impact on Statistical Properties
--------------------------------

Let the original signal :math:`x_i` have mean and variance:

.. math::

   \mu_x = \mathbb{E}[x_i], \qquad \sigma_x^2 = \mathrm{Var}(x_i)

Assume NaN values occur for indices :math:`i = s, ..., s + n - 1`, where

.. math::

   n = e - s

Effect on the Mean
------------------

The NaN offset at time :math:`i` is undefined during the fault window.
If NaN values are **ignored** when computing the mean, the observed
mean is computed over the remaining samples:

.. math::

   \mu_y = \frac{1}{N - n} \sum_{i \notin [s, e)} x_i

For a stationary signal, this yields approximately:

.. math::

   \mu_y \approx \mu_x

Effect on the Variance
----------------------

The variance of the observed signal (ignoring NaN values) is:

.. math::

   \sigma_y^2 = \frac{1}{N - n} \sum_{i \notin [s, e)} (x_i - \mu_y)^2

For stationary signals with sufficient remaining samples:

.. math::

   \sigma_y^2 \approx \sigma_x^2

Key Takeaway
------------

NaN faults preserve the underlying statistical properties of the signal
but reduce the effective sample size and may cause failures in
algorithms that do not explicitly handle missing data.

Example
-------

An example of a NaN fault compared to the true values is shown below:

.. image:: ../../images/demos/nan_fault/comparison.png
   :alt: NaN fault example
