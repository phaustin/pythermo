import site
site.addsitedir('C:\Users\Den\mya405\python\\thermlib')
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import ginput
from new_thermo import convertTempToSkew, convertSkewToTemp, thetaes, nudgePress
from convecSkew import convecSkew
from constants import constants
from calcAdiabat import calcAdiabat
from calcTvDiff import calcTvDiff

c = constants()
filename = 'littlerock.nc'
nc_file = Dataset(filename)
var_names = nc_file.variables.keys()
print var_names
print nc_file.ncattrs()
print nc_file.units
print nc_file.col_names

#get the fourth sounding
sound_var = nc_file.variables[var_names[3]]
press = sound_var[:,0]
temp = sound_var[:,2]
dewpt = sound_var[:,3]

#create the skewT-lnp graph on figure 1
fig1 = plt.figure(1)
skew, ax1 = convecSkew(1)


#get the skewed coords of the temp. and dewpoint temp.
#and plot
xdew = convertTempToSkew(dewpt, press, skew)
xtemp = convertTempToSkew(temp, press, skew)
plt.semilogy(xtemp, press, 'g', linewidth=3)
plt.semilogy(xdew, press, 'b', linewidth =3)
#**have to reset the y tick labels after using using semilogy
#**haven't found a fix for this yet
labels = np.array(range(100, 1100, 100))
ax1.set_yticks(labels)
ax1.set_yticklabels(labels)
ax1.set_ybound((400, 1000))
xlims = convertTempToSkew([-10, 30], 1.e3, skew)
ax1.set_xbound((xlims[0], xlims[1]))
ax1.set_title('littlerock sounding, %s' %var_names[3])
fig1.canvas.draw()

#get user inputed coords to draw moist adiabat
#ginput(1) returns a list with a tuple containing the coords
coords = plt.ginput(1)[0]
thePress = coords[1]
theTemp = convertSkewToTemp(coords[0], thePress, skew)
thetaeVal = thetaes(theTemp + c.Tc, thePress*100)
#pressVals in Pa, tempVals in K
pressVals, tempVals = calcAdiabat(thePress*100, thetaeVal, 400*100)
xtemp = convertTempToSkew(tempVals - c.Tc, pressVals*1e-2, skew)
#plot the adiabat
plt.semilogy(xtemp, pressVals*1e-2, 'r', linewidth=3)

#press must have unique values
newPress = nudgePress(press)
#interpolators return temp. in deg C given pressure in hPa
#newPress must be in increasing order
#env. temp. interpolator
interpTenv = lambda pVals: np.interp(pVals, newPress[::-1], temp[::-1])
#dew point temp. interpolator
interpTdenv = lambda pVals: np.interp(pVals, newPress[::-1], dewpt[::-1])
#test the interpolator
trytemp = interpTenv(pressVals*1e-2)
tryxtemp = convertTempToSkew(trytemp, pressVals*1e-2, skew)
plt.semilogy(tryxtemp, pressVals*1e-2, 'b.', markersize=3)
ax1.set_yticks(labels)
ax1.set_yticklabels(labels)
ax1.set_ybound((400, 1000))


calcTvDiffHandle = lambda pVals: calcTvDiff(pVals, thetaeVal, interpTenv, interpTdenv)
presslevs = np.linspace(400, 950, 100)*1e2
#reverse the pressure levels so integration can start at p = 950 hPa
presslevs = presslevs[::-1]
Tvdiff = np.zeros(presslevs.size)
for i in range(len(presslevs)):
    Tvdiff[i] = calcTvDiffHandle(presslevs[i])
    
plt.figure(2)
plt.plot(Tvdiff, presslevs/100)
plt.title('virtual temperature difference vs. pressure (hPa)')
plt.gca().invert_yaxis()
plt.show()


cumCAPE = -c.Rd*np.cumsum(Tvdiff[1:]*np.diff(np.log(presslevs)))

plt.figure(3)
plt.plot(cumCAPE, presslevs[1:]/100)
plt.title('cumulative CAPE (J/kg) vs. pressure (hPa)')
plt.gca().invert_yaxis()
plt.show()

#equate kinetic and potential energy toget maximum
#updraft speed
   
plt.figure(4)
maxvel=np.sqrt(2*cumCAPE);
plt.plot(maxvel, presslevs[1:]*0.01,'k-');
plt.title('maximum updraft (m/s) vs. pressure (hPa)');
plt.gca().invert_yaxis()
plt.show()
