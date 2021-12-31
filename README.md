# Documentation    
A package to compute the continuous ranked probability score (crps) (Matheson and Winkler, 1976; Hersbach, 2000), the fair-crps (fcrps) (Ferro et al., 2008), and the adjusted-crps (acrps) (Ferro et al., 2008) given an ensemble prediction and an observation.
    
The CRPS is a negatively oriented score that is used to compare the empirical distribution of an ensemble prediction to a scalar observation.

References:
[1] Matheson, J. E. & Winkler, R. L. Scoring Rules for Continuous Probability Distributions. Management Science 22, 1087–1096 (1976).

[2] Hersbach, H. Decomposition of the Continuous Ranked Probability Score for Ensemble Prediction Systems. Wea. Forecasting 15, 559–570 (2000).

[3] Ferro, C. A. T., Richardson, D. S. & Weigel, A. P. On the effect of ensemble size on the discrete and continuous ranked probability scores. Meteorological Applications 15, 19–24 (2008).

## _Installation:_
```sh
pip install continuous-ranked-probability-score
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

## _Methods:_
**compute()**:
Computes the continuous ranked probability score (crps), the fair-crps (fcrps), and the adjusted-crps (acrps).

_Returns_:
crps,fcrps,acrps

## _Attributes:_
**cdf_fc**: 
Empirical cumulative distribution function ([CDF](https://en.wikipedia.org/wiki/Cumulative_distribution_function)) of the forecasts (y). F(y) in the crps equation.
   
**cdf_ob**:
CDF ([heaviside step function](https://en.wikipedia.org/wiki/Heaviside_step_function)) for the observation (o). It takes 0 for values is less than the observation, and 1 otherwise. F<sub>o</sub>(y) in the crps equation.
    
**delta_fc**:
dy term in the crps equation.
    
**crps**: Continuous Ranked Probability Score
It is the integral of the squared difference between the CDF of the forecasts and the observation.

![crps](http://www.sciweavers.org/tex2img.php?eq=crps%20%3D%20%20%5Cint_%7B-%5Cinfty%7D%5E%7B%5Cinfty%7D%20%5BF%28y%29%20-%20F_%7Bo%7D%28y%29%5D%5E2%20dy%20&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)

**fcrps**: Fair-Continuous Ranked Probability Score
It is the crps computed assuming an infinite ensemble size.

![fcrps](http://www.sciweavers.org/tex2img.php?eq=fcrps%20%3D%20crps%20-%20%20%5Cint_%7B-%5Cinfty%7D%5E%7B%5Cinfty%7D%20%5BF%28y%29%20%281%20-%20F%28y%29%29%2F%28m-1%29%5D%20dy&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)

where m is the current ensemble size (i.e., len(ensemble_members))

**acrps**: Adjusted-Continuous Ranked Probability Score
It is the crps computed assuming an ensemble size of M.

![acrps](http://www.sciweavers.org/tex2img.php?eq=acrps%20%3D%20crps%20-%20%20%5Cint_%7B-%5Cinfty%7D%5E%7B%5Cinfty%7D%20%5B%281%20-%20m%2FM%29%20F%28y%29%20%281%20-%20F%28y%29%29%2F%28m-1%29%5D%20dy&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)

where M is the adjusted_ensemble_size

## _Demonstration:_
```sh
import numpy as np
import continuous-ranked-probability-score.CRPS as pscore
```
Example - 1
```sh
In [1]: CRPS(np.random.uniform(2,5,50),3.5).compute()
Out[1]: (0.24374216742963792, 0.2332762342590258, 0.23589271755167882)
```
Example - 2
```sh
In [2]: crps,fcrps,acrps = CRPS(np.random.uniform(1.2,7,100),8.3,50).compute()
In [3]: crps
Out[3]: 3.11890267263096
In [4]: fcrps
Out[4]: 3.109573704801023
In [5]: acrps
Out[5]: 3.129164537243891
```

