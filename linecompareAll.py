# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot  as plt
from datetime import datetime

    
def readObjList(path):
    objList=[]
    pathDir =  os.listdir(path)
    for allDir in pathDir:
        child = os.path.join('%s\\%s' % (path, allDir))
        f = open(child,"r")  
        lines = f.readlines()
        
        objrecord=[]
        for line in lines:
            tlist = line.split(',')
            if(tlist[2].find('.')==-1):
                objrecord.append([np.float32(tlist[0]), np.float32(tlist[1]), 
                                           (datetime.strptime(tlist[2], '%Y-%m-%d %H:%M:%S')-datetime(1970,1,1)).total_seconds(), np.int32(tlist[5])])
            else:
                objrecord.append([np.float32(tlist[0]), np.float32(tlist[1]), 
                                           (datetime.strptime(tlist[2], '%Y-%m-%d %H:%M:%S.%f')-datetime(1970,1,1)).total_seconds(), np.int32(tlist[5])])
        objList.append({'name':allDir, 'data':np.array(objrecord)})
        f.close()
    return objList
    
def readObj(path):
    objrecord=[]
    f = open(path,"r")  
    lines = f.readlines()
    
    idx=1
    for line in lines:
        if(idx%30==1):
            tlist = line.split()
            if(tlist[2].find('60')==-1):
                if(tlist[2].find('.')==-1):
                    objrecord.append([np.float32(tlist[3]), np.float32(tlist[4]), 
                                               (datetime.strptime(tlist[1]+' '+tlist[2], '%Y-%m-%d %H:%M:%S')-datetime(1970,1,1)).total_seconds()])
                else:
                    objrecord.append([np.float32(tlist[3]), np.float32(tlist[4]), 
                                               (datetime.strptime(tlist[1]+' '+tlist[2], '%Y-%m-%d %H:%M:%S.%f')-datetime(1970,1,1)).total_seconds()])
        idx=idx+1
    f.close()
    return np.array(objrecord)
        
def polyfit(x, y, degree):
    results = {}
    coeffs = np.polyfit(x, y, degree)
    results['polynomiline'] = coeffs.tolist()

    p = np.poly1d(coeffs)
    yfit = p(x)
    ysub = np.abs(y-yfit)
    ysavg = np.sum(ysub)/len(ysub)
    ssreg = np.sum((ysub-ysavg)**2)/len(y)
    results['sdev'] = np.sqrt(ssreg)
    results['subavg'] = ysavg
    results['submin'] = np.min(ysub)
    results['submax'] = np.max(ysub)
    return results
    
def polyfit2(x, y, coeffs):
    results = {}

    p = np.poly1d(coeffs)
    yfit = p(x)
    ysub = np.abs(y-yfit)
    ysavg = np.sum(ysub)/len(ysub)
    ssreg = np.sum((ysub-ysavg)**2)/len(y)
    results['sdev'] = np.sqrt(ssreg)
    results['subavg'] = ysavg
    results['submin'] = np.min(ysub)
    results['submax'] = np.max(ysub)
    return results
    
def matchObj(objList, path2):

    matchList=[]
    radecfit=[]
    ratfit=[]
    dectfit=[]
    matchObjs=[]
    
    for i, val in enumerate(objList):
        ra=val['data'][:,0]
        dec=val['data'][:,1]
        date=val['data'][:,2]
        tfit=polyfit(ra, dec, 2)
        tfit['minra'] = np.min(ra)
        tfit['maxra'] = np.max(ra)
        tfit['mindec'] = np.min(dec)
        tfit['maxdec'] = np.max(dec)
        tfit['mindate'] = np.min(date)
        tfit['maxdate'] = np.max(date)
        radecfit.append(tfit)
        
        tfit2=polyfit(ra, date, 2)
        ratfit.append(tfit2)
        tfit3=polyfit(dec, date, 2)
        dectfit.append(tfit3)

    pathDir =  os.listdir(path2)
    for j, allDir in enumerate(pathDir):
        child = os.path.join('%s\\%s' % (path2, allDir))
        objrecords = readObj(child)
        ra=objrecords[:,0]
        dec=objrecords[:,1]
        date=objrecords[:,2]
        
        for i, val in enumerate(radecfit):
            trecs=objrecords[(ra>=val['minra'])&(ra<=val['maxra'])&(dec>=val['mindec'])&(dec<=val['maxdec'])]
            if(trecs.shape[0]>10):
                radec = polyfit2(trecs[:,0], trecs[:,1], val['polynomiline'])
                if radec['subavg']<60.0/3600 and radec['submax']<120.0/3600:
                    ratime = polyfit2(trecs[:,0], trecs[:,2], ratfit[i]['polynomiline'])
                    dectime = polyfit2(trecs[:,1], trecs[:,2], dectfit[i]['polynomiline'])
                    matchList.append([int(objList[i]['data'][0][3]), int(i), int(j), radec['subavg'], radec['submax'], ratime['subavg'], ratime['submax'], 
                    dectime['subavg'], dectime['submax']])
                    matchObjs.append(objrecords)
                    #matchObjs.append(trecs)
    
    matchList=np.array(matchList)
    matchObjs=np.array(matchObjs)
    return matchList, matchObjs
    
def showTime(matchList):
    fig,ax = plt.subplots()  
    plt.xlabel('Index')  
    plt.ylabel('time offset (second)')
    
    for i in range(1,13):
        tlist = matchList[(matchList[:,0]==i) & (matchList[:,5]<100)]
        objNum = len(tlist)
        if(objNum>0):
            x = [x for x in range(1,objNum+1)]
            plt.plot(x,tlist[:,5],"-",label="CCD"+str(i)) 
            
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)  
    plt.show()  
        
def showPos(matchList, matchObjs, objList):
    fig,ax = plt.subplots()  
    plt.xlabel('ra (deg)')  
    plt.ylabel('dec (deg)')
    
    for i in range(1,13):
        tlist = matchList[(matchList[:,0]==i) & (matchList[:,5]<100)]
        objlist = matchObjs[(matchList[:,0]==i) & (matchList[:,5]<100)]
        objNum = len(tlist)
        if(objNum>0):
            for j, mtch in enumerate(tlist):
                obj1=objList[int(mtch[1])]['data']
                obj2=objlist[j]
                #print(obj1.shape)
                #print(obj2.shape)
                plt.plot(obj1[:,0],obj1[:,1],"*") 
                plt.plot(obj2[:,0],obj2[:,1],".") 
            
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)  
    plt.show()  
    
def saveToFile(matchList, matchObjs, objList):
    mlist = matchList[matchList[:,5]<100]
    objlist = matchObjs[matchList[:,5]<100]
    #mlist = matchList
    #objlist = matchObjs
    print("gwac data: "+str(matchList.shape[0])+" valid "+str(mlist.shape[0]))
    print("othe data: "+str(matchObjs.shape[0])+" valid "+str(objlist.shape[0]))
    
    gwacData=np.array(objList)[mlist[:,1].astype(int).tolist()]
    data2=objlist
    with open('gwacdata-min5.txt',"w") as f:
        f.write("\n".join("\n".join(map(str, x['data'][:,0:2])) for x in gwacData))
    with open('data2-min5.txt',"w") as f:
        f.write("\n".join("\n".join(map(str, x[:,0:2])) for x in objlist))
    

    
path1='E:\\linecompare\\161228_220'
#path1='E:\\linecompare\\161228_392-min10'
#path1='E:\\linecompare\\161228_580-min5'
path2='E:\\linecompare\\2016-12-28'

objList=readObjList(path1)
matchList, matchObjs=matchObj(objList, path2)

#showTime(matchList)
#showPos(matchList, matchObjs, objList)
saveToFile(matchList, matchObjs, objList)

