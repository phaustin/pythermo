"""This is the docstring for the calcAdiabat.py module."""

import constants as c
import numpy as np
from new_thermo import findTmoist

def calcAdiabat(press0, thetae0, topPress):
    """
    
    Calculates the temperature-pressure coordinates of a moist adiabat.
    
    Parameters
    - - - - - -
    press0: the initial pressure (Pa)
    thetae0: the equivalent potential temperature (K) of the adiabat
    topPress: the final pressure (Pa)
    
    Returns
    - - - - - -
    (pressVals, tempVals): pressVals (Pa) and tempVals (K) are 50 x 1 arrays 
                           and are the coordinates of the thetae0 adiabat
                
    
    Tests
    - - - - -
    >>> p,T = calcAdiabat(800*100, 300, 1000*100)
    >>> p.shape
    (50,)
    >>> T.shape
    (50,)
    

    """
    
    pressVals = np.linspace(press0, topPress, 50)
    tempVals = np.zeros(pressVals.size)
    
    for i in range(pressVals.size):
        tempVals[i] = findTmoist(thetae0, pressVals[i])
    
    return pressVals, tempVals

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

     
         
        
    
    
    
    