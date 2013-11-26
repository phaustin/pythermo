try:
    from sounding_dir.readsoundings import readsound
except ImportError:
    import sys
    sys.path.append('/home/phil/repos')
    from sounding_dir.readsoundings import readsound
import datetime
import dateutil
    
import numpy as np
import string
from scipy.io import savemat
import glob
import matplotlib.pyplot as plt
import pickle

listfiles=glob.glob('littlerock*txt')
sounding_times=[]
for a_file in listfiles:
    print "*"*60
    print "working on: ",a_file
    out=readsound(a_file)
    thekeys=out.keys()
    thekeys.sort()
    keyList=[]
    titleList=[]
    datevecList=[]
    for key in thekeys:
        print "working on: ",key
        oldTup=key.split()
        newTup=(oldTup[2],oldTup[1],oldTup[3],oldTup[0])
        #rearrange:  ('Jul', '31',  '2010','12Z')
        print "rearrange: ",newTup
        #remove spaces to make valid matlab varname
        newkey='%s-%s-%s-%s' % newTup
        #switch to dashes for plot titles that don't subscript
        plotTitle='%s-%s-%s-%s' % newTup
        theDay=int(newTup[1])
        theTime=int(newTup[2][:2])
        #use (day,time) for sorting
        test=(newTup,(theDay,theTime))
        print "debug thesounding: ",test
        datevecList.append(test)
        keyList.append((newTup,(key,newkey)))
        titleList.append((newTup,plotTitle))
    datevecList.sort()
    keyList.sort()
    titleList.sort()
    #undecorate
    keyList=[item for newTup,item in keyList]
    titleList=[item for newTup,item in titleList]
    datevecList=[item for newTup,item in datevecList]
    newDict={}
    #
    # old has spaces, new has underlines
    #
    colnames=('press','height','temp','dewpt','relh','mixr','drct',\
              'sknt')
    titles=('hPa','height_m','temp_C','dewpt_C','relh_percent','mixr_gperkg',\
            'deg','knot')
    for old,new in keyList:
        #grab the first 8 columns
        ## [,0] PRES(hPa); [,1] HGHT(m); [,2] TEMP[C];
        ## [,3] DWPT(C); [,4] RELH(%); [,5] MIXR(g/kg);
        titles=('hPa','height_m','temp_C','dewpt_C','relh_percent','mixr_gperkg',\
            'deg','knot')
        the_array=out[old][:,:8]
        print "new: ",old,new
        print "titles: ",titles
        print "colnames: ",colnames
        newDict[new]=np.rec.fromarrays(the_array.T,names=colnames,titles=titles)
        print "col check: ",newDict[new].dtype.names
        print "col names: ",newDict[new].dtype.fields.items()

    newname=a_file.replace('txt','pic')
    outfile=open(newname,'w')
    outDict={'filename':a_file,'data':newDict}
    pickle.dump(outDict,outfile)
    outfile.close()
