"""This is the docstring for the calcTvDiff.py module."""

import site
site.addsitedir('C:\Users\Den\mya405\python\\thermlib')
from constants import constants
import numpy as np
from new_thermo import findTmoist, wsat

def calcTvDiff(press, thetae0, interpTenv, interpTdEnv):
    """
    
    Calculates the virtual temperature difference between the thetae0
    moist adiabat and a given sounding at some pressure.
    
    Parameters
    - - - - - -
    
    press: pressure (Pa)
    thetae0: equivalent potential temperature of the adiabat (K)
    interpTenv: interpolator for environmental temperature (deg C)
    interpTdEnv: interpolator for environmental dew point temperature (deg C)
    
    Returns
    - - - - - -
    TvDiff: the virtual temperature difference at pressure press 
    between the thetae0 moist adiabat and the given sounding (K).
    
   
    """
    
    c = constants()
    Tcloud=findTmoist(thetae0,press)
    wvcloud=wsat(Tcloud,press)
    Tvcloud=Tcloud*(1. + c.eps*wvcloud)
    Tenv=interpTenv(press*1.e-2) + c.Tc
    Tdenv=interpTdEnv(press*1.e-2) + c.Tc
    wvenv=wsat(Tdenv,press)
    Tvenv=Tenv*(1. + c.eps*wvenv)
    return Tvcloud - Tvenv
    
    