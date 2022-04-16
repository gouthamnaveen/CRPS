# Documentation  

A package to compute the continuous ranked probability score (crps) (Matheson and Winkler, 1976; Hersbach, 2000), the fair-crps (fcrps) (Ferro et al., 2008), and the adjusted-crps (acrps) (Ferro et al., 2008) given an ensemble prediction and an observation.
    
The CRPS is a negatively oriented score that is used to compare the empirical distribution of an ensemble prediction to a scalar observation. 

Read documentation at [https://github.com/garovent/CRPS](https://github.com/garovent/CRPS)

_References_:

[1] Matheson, J. E. & Winkler, R. L. Scoring Rules for Continuous Probability Distributions. Management Science 22, 1087–1096 (1976).

[2] Hersbach, H. Decomposition of the Continuous Ranked Probability Score for Ensemble Prediction Systems. Wea. Forecasting 15, 559–570 (2000).

[3] Ferro, C. A. T., Richardson, D. S. & Weigel, A. P. On the effect of ensemble size on the discrete and continuous ranked probability scores. Meteorological Applications 15, 19–24 (2008).

## _Installation:_

```sh
pip install CRPS
```

## _Parameters:_

**ensemble_members**: numpy.ndarray

The predicted ensemble members. They will be sorted in ascending order automatically.

Ex: np.array([2.1,3.5,4.7,1.2,1.3,5.2,5.3,4.2,3.1,1.7])

**observation**: float

The observed scalar.

Ex: 5.4
    
**adjusted_ensemble_size**: int, optional

The size the ensemble needs to be adjusted to before computing the Adjusted Continuous Ranked Probability Score. The default is 200. 

_Note_: The crps becomes equal to acrps when adjusted_ensemble_size equals the length of the ensemble_members.

## _Method(s):_

**compute()**:

Computes the continuous ranked probability score (crps), the fair-crps (fcrps), and the adjusted-crps (acrps).

_Returns_:

crps,fcrps,acrps

## _Attributes:_
    
**crps**: Continuous Ranked Probability Score

It is the integral of the squared difference between the CDF of the forecast ensemble and the observation.

![crps](crps.jpg)

**fcrps**: Fair-Continuous Ranked Probability Score

It is the crps computed assuming an infinite ensemble size.

![fcrps](fcrps.jpg)

where m is the current ensemble size (i.e., len(ensemble_members))

**acrps**: Adjusted-Continuous Ranked Probability Score

It is the crps computed assuming an ensemble size of M.

![acrps](acrps.jpg)

where M is the adjusted_ensemble_size

## _Demonstration:_

```sh
import numpy as np
import CRPS.CRPS as pscore
```

Example - 1:
```sh
In [1]: pscore(np.arange(1,5),3.5).compute()
Out[1]: (0.625, 0.4166666666666667, 0.42083333333333334)
```

Example - 2:
```sh
In [2]: crps,fcrps,acrps = pscore(np.arange(1,11),8.3,50).compute()
In [3]: crps
Out[3]: 1.6300000000000003
In [4]: fcrps
Out[4]: 1.446666666666667
In [5]: acrps
Out[5]: 1.4833333333333336
```

