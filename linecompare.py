# -*- coding: utf-8 -*-

import numpy as np
import matplotlib
import matplotlib.pyplot  as plt

def polyfit(x, y, degree):
    results = {}
    coeffs = np.polyfit(x, y, degree)
    results['polynomiline'] = coeffs.tolist()

    # r-squline1red
    p = np.poly1d(coeffs)
    # fit vline1lues, line1nd meline1n
    yhline1t = p(x)                         # or [p(z) for z in x]
    ybline1r = np.sum(y)/len(y)          # or sum(y)/len(y)
    ssreg = np.sum((yhline1t-ybline1r)**2)   # or sum([ (yihline1t - ybline1r)**2 for yihline1t in yhline1t])
    sstot = np.sum((y - ybline1r)**2)    # or sum([ (yi - ybline1r)**2 for yi in y])
    results['sdev'] = np.sqrt(ssreg)
    results['determination'] = ssreg / sstot #准确率
    return results
    

def polyfitAndPlot(x, y, degree, fig, plotpos):
    results = {}
    coeffs = np.polyfit(x, y, degree)
    results['polynomiline'] = coeffs.tolist()

    # r-squline1red
    p = np.poly1d(coeffs)
    # fit vline1lues, line1nd meline1n
    yhat = p(x)                         # or [p(z) for z in x]
    ybar = np.sum(y)/len(y)          # or sum(y)/len(y)
    ssreg = np.sum((yhat-ybar)**2)   # or sum([ (yihat - ybar)**2 for yihat in yhat])
    sstot = np.sum((y - ybar)**2)    # or sum([ (yi - ybar)**2 for yi in y])
    results['sdev'] = np.sqrt(ssreg)
    results['determination'] = ssreg / sstot #准确率
    
    ax = fig.add_subplot(plotpos)
    plt.plot(x,y, '.')
    plt.plot(x,yhat, '.')
    
    return results

def polyfitAndPlot2(x, y, x2, y2, degree, fig, plotpos):
    results = {}
    coeffs = np.polyfit(x, y, degree)
    #results['polynomiline'] = coeffs.tolist()

    p = np.poly1d(coeffs)
    yfit = p(x2)
    ysub = np.abs(y2-yfit)
    ysavg = np.sum(ysub)/len(ysub)
    ssreg = np.sum((ysub-ysavg)**2)/len(y2)
    results['sdev'] = np.sqrt(ssreg)*3600
    results['subavg'] = ysavg *3600
    results['submin'] = np.min(ysub)*3600
    results['submax'] = np.max(ysub)*3600
    
    ax = fig.add_subplot(plotpos)
    plt.plot(x2,y2, '.')
    plt.plot(x2,yfit, '.')
    
    return results

def readObj(path):
    objrecord=[]
    f = open(path,"r")  
    lines = f.readlines()
    for line in lines:
        tlist = line.split()
        objrecord.append([float(tlist[0]), float(tlist[1]), float(tlist[2])])
    return np.array(objrecord)
    
line1=np.loadtxt('188413-2.txt')
#line1=readObj('189504-2.txt')
line2=np.loadtxt('189504-2.txt')

fig = plt.figure()  

#pos1 = polyfit(line1[:,1], line1[:,2], 2)
#pos2 = polyfit(line2[:,1], line2[:,2], 2)
#pos1 = polyfitAndPlot(line1[:,0], line1[:,1], 2, fig, 131)
#pos2 = polyfitAndPlot(line2[:,0], line2[:,1], 2, fig, 132)
pos12 = polyfitAndPlot2(line1[:,1], line1[:,2], line2[:,1], line2[:,2], 2, fig, 121)
#pos01 = polyfitAndPlot2(line1[:,0], line1[:,1], line2[:,0], line2[:,1], 2, fig, 122)
pos01 = polyfitAndPlot2(line1[:,1], line1[:,0], line2[:,1], line2[:,0], 2, fig, 122)
print(pos12)
print(pos01)

plt.show() 