Documentation
=============    
A package to compute the Continuous Ranked Probability Score (crps) (Matheson and Winkler, 1976; Hersbach, 2000), the fair-crps (fcrps) (Ferro et al., 2008), and the adjusted-crps (acrps) (Ferro et al., 2008) given an ensemble prediction and an observation.
    
The continuous ranked probability score is a negatively oriented score that is used to compare the empirical distribution of an ensemble prediction to a scalar observation.

References:
[1] Matheson, J. E. & Winkler, R. L. Scoring Rules for Continuous Probability Distributions. Management Science 22, 1087–1096 (1976).
[2] Hersbach, H. Decomposition of the Continuous Ranked Probability Score for Ensemble Prediction Systems. Wea. Forecasting 15, 559–570 (2000).
[3] Ferro, C. A. T., Richardson, D. S. & Weigel, A. P. On the effect of ensemble size on the discrete and continuous ranked probability scores. Meteorological Applications 15, 19–24 (2008).

Installation
------------
``pip install continuous-ranked-probability-score``
    
Parameters
----------
**ensemble_members**: numpy.ndarray
The predicted ensemble members. They will be sorted in ascending order automatically.
Ex: np.array([2.1,3.5,4.7,1.2,1.3,5.2,5.3,4.2,3.1,1.7])

**observation**: float
The observed scalar.
Ex: 5.4
    
**adjusted_ensemble_size**: int, optional
The size the ensemble needs to be adjusted to before computing the Adjusted Continuous Ranked Probability Score. The default is 200. 
*Note*: The crps becomes equal to acrps when adjusted_ensemble_size equals the length of the ensemble_members.

Methods
-------
**compute()**:
Computes the continuous ranked probability score (crps), the fair-crps (fcrps), and the adjusted-crps (acrps).

*Returns*:
crps,fcrps,acrps

Attributes
----------
**cdf_fc**: 
Empirical cumulative distribution function (`CDF`_) of the forecasts (y). F(y) in the crps equation.
   
**cdf_ob**:
CDF (`heaviside step function`_) for the observation (o). It takes 0 for values is less than the observation, and 1 otherwise. :math:`F_{o}(y)` in the crps equation.
    
**delta_fc**:
dy term in the crps equation.
    
**crps**: Continuous Ranked Probability Score
It is the integral of the squared difference between the CDF of the forecasts and the observation.
.. math:: crps = \int\limits_{-\infty}^{\infty} [F(y) - F_{o}(y)]^2 dy

**fcrps**: Fair-Continuous Ranked Probability Score
It is the crps computed assuming an infinite ensemble size.
.. math:: fcrps = crps - \int_{-\infty}^{\infty} [F(y) (1 - F(y))/(m-1)] dy
where m is the current ensemble size (i.e., len(ensemble_members))

**acrps**: Adjusted-Continuous Ranked Probability Score
It is the crps computed assuming an ensemble size of M.
.. math:: acrps = crps - \int_{-\infty}^{\infty} [(1 - m/M) F(y) (1 - F(y))/(m-1)] dy
where M is the adjusted_ensemble_size

.. _CDF: https://en.wikipedia.org/wiki/Cumulative_distribution_function
.. _heaviside step function: https://en.wikipedia.org/wiki/Heaviside_step_function


Demonstration
-------------
``
import numpy as np
import continuous-ranked-probability-score.CRPS as pscore
``

Example 1
``
In [1]: pscore(np.random.uniform(2,5,50),3.5).compute()
Out[1]: (0.24374216742963792, 0.2332762342590258, 0.23589271755167882)
``

Example 2
``
In [2]: crps,fcrps,acrps = pscore(np.random.uniform(1.2,7,100),8.3,50).compute()
In [3]: crps
Out[3]: 3.11890267263096
In [4]: fcrps
Out[4]: 3.109573704801023
In [5]: acrps
Out[5]: 3.129164537243891
``


