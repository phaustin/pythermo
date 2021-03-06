import site
site.addsitedir('C:\Users\Den\mya405\python\\thermlib')
import numpy as np
import matplotlib.pyplot as plt
from constants import constants
from new_thermo import findTdwv, thetaep, tinvert_thetae, wsat, convertTempToSkew
from convecSkew import convecSkew


c = constants();

eqT_bot=30 + c.Tc
eqwv_bot=14*1.e-3
sfT_bot=21 + c.Tc
sfwv_bot=3.e-3
eqwv_top=3.e-3
sfwv_top=3.e-3
ptop=410.e2
pbot=1000.e2

eqTd_bot=findTdwv(eqwv_bot,pbot)
sfTd_bot=findTdwv(sfwv_bot,pbot)
thetae_eq=thetaep(eqTd_bot,eqT_bot,pbot)
thetae_sf=thetaep(sfTd_bot,sfT_bot,pbot)

fig1 = plt.figure(1)
skew, ax1 = convecSkew(1)


pvec=np.arange(ptop, pbot, 1000)
#initialize vectors
Tvec_eq = np.zeros(pvec.size)
Tvec_sf = np.zeros(pvec.size)
wv = np.zeros(pvec.size)
wl = np.zeros(pvec.size)
xcoord_eq = np.zeros(pvec.size)
xcoord_sf = np.zeros(pvec.size)

for i in range(0, len(pvec)):
    Tvec_eq[i], wv[i], wl[i] = tinvert_thetae(thetae_eq, eqwv_bot, pvec[i])
    xcoord_eq[i] = convertTempToSkew(Tvec_eq[i] - c.Tc, pvec[i]*0.01, skew)
    Tvec_sf[i], wv[i], wl[i] = tinvert_thetae(thetae_sf, sfwv_bot, pvec[i])
    xcoord_sf[i] = convertTempToSkew(Tvec_sf[i] - c.Tc, pvec[i]*0.01, skew)
    
    
tempA=Tvec_sf[len(Tvec_sf)-1]
pressA=pbot
tempB=Tvec_eq[len(Tvec_eq)-1]
pressB=pbot
tempC=Tvec_eq[0]
pressC=ptop
tempD=Tvec_sf[0]
pressD=ptop;
wvD=wsat(tempD,ptop)
wvC=wsat(tempC,ptop)
    
hot_adiabat=plt.plot(xcoord_eq,pvec*0.01,'r-',linewidth=3)
cold_adiabat=plt.plot(xcoord_sf,pvec*0.01,'b-', linewidth=3)
plt.axis([convertTempToSkew(-15.,1000.,skew), 
        convertTempToSkew(35.,1000.,skew), 1020, 350])

xtempA=convertTempToSkew(tempA - c.Tc,pressA*0.01,skew);
xtempB=convertTempToSkew(tempB - c.Tc,pressB*0.01,skew);
xtempC=convertTempToSkew(tempC - c.Tc,pressC*0.01,skew);
xtempD=convertTempToSkew(tempD - c.Tc,pressD*0.01,skew);


plt.text(xtempA,pressA*0.01,'A', fontweight='bold',fontsize= 22, color='b');
plt.text(xtempB,pressB*0.01,'B', fontweight='bold',fontsize= 22,color='b');
plt.text(xtempC,pressC*0.01,'C', fontweight='bold',fontsize= 22,color='b');
plt.text(xtempD,pressD*0.01,'D', fontweight='bold',fontsize= 22, color='b');


plt.title('heat engine (hadley cell?)')
plt.legend(('equator', 'san francisco'))
plt.show()