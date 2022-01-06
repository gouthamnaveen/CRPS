#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 6 09:19:41 2021

@author: Naveen GOUTHAM
"""
import numpy as np

class CRPS:
    '''
    A class to compute the continuous ranked probability score (crps) (Matheson and Winkler, 1976; Hersbach, 2000), the fair-crps (fcrps) (Ferro et al., 2008), and the adjusted-crps (acrps) (Ferro et al., 2008) given an ensemble prediction and an observation.
        
    The CRPS is a negatively oriented score that is used to compare the empirical distribution of an ensemble prediction to a scalar observation.
    
    References:
        [1] Matheson, J. E. & Winkler, R. L. Scoring Rules for Continuous Probability Distributions. Management Science 22, 1087–1096 (1976).
        [2] Hersbach, H. Decomposition of the Continuous Ranked Probability Score for Ensemble Prediction Systems. Wea. Forecasting 15, 559–570 (2000).
        [3] Ferro, C. A. T., Richardson, D. S. & Weigel, A. P. On the effect of ensemble size on the discrete and continuous ranked probability scores. Meteorological Applications 15, 19–24 (2008).

    ----------
    
    Parameters:
        ensemble_members: numpy.ndarray
            The predicted ensemble members. They will be sorted in ascending order automatically.
            Ex: np.array([2.1,3.5,4.7,1.2,1.3,5.2,5.3,4.2,3.1,1.7])
            
        observation: float
            The observed value.
            Ex: 5.4
            
        adjusted_ensemble_size: int, optional
            The size the ensemble needs to be adjusted to before computing the Adjusted Continuous Ranked Probability Score.
            The default is 200. 
            Note: The crps becomes equal to acrps when adjusted_ensemble_size equals the length of the ensemble_members.
    
    ----------
    
    Methods:
            
        compute():
            Computes the continuous ranked probability score (crps), the fair-crps (fcrps), and the adjusted-crps (acrps).

    ----------
            
    Attributes:
        cdf_fc: 
            Empirical cumulative distribution function (cdf) of the forecasts (y). F(y) in the crps equation.
        
        cdf_ob:
            CDF (heaviside step function) for the observation (o). 
        
        delta_fc:
            dy term in the crps equation.
        
        crps: Continuous Ranked Probability Score
            It is the integral of the squared difference between the CDF of the forecast ensemble and the observation.
            
            .. math:: 
            \mathrm{crps = \int_{-\infty}^{\infty} [F(y) - F_{o}(y)]^2 dy}
          
        fcrps: Fair-Continuous Ranked Probability Score
            It is the crps computed assuming an infinite ensemble size.
            
            .. math::
            \mathrm{fcrps = crps - \int_{-\infty}^{\infty} [F(y) (1 - F(y))/(m-1)] dy},
            
            where m is the current ensemble size (here: length of ensemble_members)

        acrps: Adjusted-Continuous Ranked Probability Score
            It is the crps computed assuming an ensemble size of M.
            
            .. math::
            \mathrm{acrps = crps - \int_{-\infty}^{\infty} [(1 - m/M) F(y) (1 - F(y))/(m-1)] dy},
            
            where M is the adjusted_ensemble_size
            
    ----------
    
    Demonstration:
    	import numpy as np
	import CRPS.CRPS as pscore

	Example - 1:
	In [1]: pscore(np.random.uniform(2,5,50),3.5).compute()
	Out[1]: (0.24374216742963792, 0.2332762342590258, 0.23589271755167882)

	Example - 2:
	In [2]: crps,fcrps,acrps = pscore(np.random.uniform(1.2,7,100),8.3,50).compute()
	In [3]: crps
	Out[3]: 3.11890267263096
	In [4]: fcrps
	Out[4]: 3.109573704801023
	In [5]: acrps
	Out[5]: 3.129164537243891
        
    '''
    def __init__(self,ensemble_members,observation,adjusted_ensemble_size=200):
        '''
        Parameters:
            ensemble_members: numpy.ndarray
                The predicted ensemble members.
                Ex: np.array([2.1,3.5,4.7,1.2,1.3,5.2,5.3,4.2,3.1,1.7])
            observation: float
                The observed value.
                Ex: 5.4
            adjusted_ensemble_size: int, optional
                The size the ensemble needs to be adjusted to before computing the Adjusted Continuous Ranked Probability Score.
                The default is 200. 
                Note: The crps becomes equal to acrps when adjusted_ensemble_size equals the length of the ensemble_members.
        
        Returns:
            None
            
        '''
        self.fc = np.sort(ensemble_members)
        self.ob = observation
        self.M = int(adjusted_ensemble_size)
        self.cdf_fc = None
        self.cdf_ob = None
        self.delta_fc = None
        self.crps = None
        self.fcrps = None
        self.acrps = None
        
    def __str__(self):
        "Kindly refer to the __doc__ method for documentation. i.e. print(CRPS.__doc__)."
            
    def __build_cdf_fc(self):
        '''
        This method builds the empirical cumulative distribution function (cdf) for any given ensemble size.
        
        Returns:
            None
        
        Attributes:
            cdf_fc
        
        '''
        mem_fc = len(self.fc)
        cdf_fc = []
        cdf_fc_in = 0
        k = 0
        for k in range(mem_fc):
            val = (1/mem_fc) + cdf_fc_in
            cdf_fc_in = val
            cdf_fc.append(val)
        cdf_fc = np.array(cdf_fc)
        self.cdf_fc = cdf_fc
        return None
        
    def __fix_ends(self):
        '''
        This method checks if the observed value is within the ensemble distribution. If the observation falls outside of the ensemble distribution, this method adjusts the tails of the distribution to include the observation.
        
        Returns:
            None
        
        '''
        self.__build_cdf_fc()
        if self.fc[-1] < self.ob:
            self.fc = np.array(list(self.fc) + list(np.linspace(self.fc[-1],self.ob,5)), dtype=object)
            self.cdf_fc = np.array(list(self.cdf_fc) + list(np.ones(5)), dtype=object)
        if self.fc[0] > self.ob:
            self.fc = np.array(list(np.linspace(self.ob,self.fc[0],5)) + list(self.fc), dtype=object)
            self.cdf_fc = np.array(list(np.zeros(5)) + list(self.cdf_fc), dtype=object)
        return None
    
    def __build_cdf_ob(self):
        '''
        This method builds the cumulative distribution function (cdf) for the observation as a heaviside step function.
        
        Returns:
            None
        
        Attributes:
            cdf_ob   
        
        '''
        self.__fix_ends()
        self.cdf_ob = (self.fc >= self.ob)
        return None
    
    def __delta(self):
        '''
        This method computes delta (i.e., difference) between the adjacent ensemble members.

        Returns:
            None

        Attributes:
            delta_fc
            
        '''
        self.delta_fc = np.array([self.fc[m+1] - self.fc[m] for m in range(len(self.fc)-1)] + list(np.zeros(1)), dtype=object)
        return None
    
    def compute(self):
        '''
        This method computes the continuous ranked probability score (crps), the fair-crps (fcrps), and the adjusted-crps (acrps).

        Returns:
            crps, fcrps, acrps

        Attributes:
            crps, fcrps, acrps

        '''
        self.__build_cdf_ob()
        self.__delta()
        self.crps = np.sum(np.array((self.cdf_fc - self.cdf_ob) ** 2)*self.delta_fc)
        m = len(self.cdf_fc)
        self.fcrps = self.crps - np.sum(np.array(((self.cdf_fc * (1 - self.cdf_fc))/(m-1))*self.delta_fc))
        self.acrps = self.crps - np.sum(np.array((((1 - (m/self.M)) * self.cdf_fc * (1 - self.cdf_fc))/(m-1))*self.delta_fc))
        return self.crps, self.fcrps, self.acrps
