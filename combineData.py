# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot  as plt
    
def combineAll(path, fname):
    
    pathDir =  os.listdir(path)
    fw = open(fname,"w")
    
    for allDir in pathDir:
        child = os.path.join('%s\\%s' % (path, allDir))
        f = open(child, 'r', encoding='utf-8', errors='ignore')  
        lines = f.readlines()
        
        for i, line in enumerate(lines):
            if i>6:
                fw.write(line)
        f.close()
    fw.close
    
path1='E:\\work\\program\\python\\linecompare\\matched'
fname='allInOne.txt'
combineAll(path1, fname)