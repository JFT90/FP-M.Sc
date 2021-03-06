#!/usr/bin/python3
# -*- coding: utf-8 -*-

output_silent = False

import numpy as np
from scipy import optimize, interpolate, misc, stats, constants
import os
import sys
import re
import matplotlib.pyplot as plt
import scipy.optimize as optimization
import math
import matplotlib.cm as cm

for arg in sys.argv:
    if(arg=='silent'):
        output_silent = True

#########################################
# Preparation				#
#########################################

def Mt1(t,y0,y1,y2,T21,T22,beta1,beta2):
    #return y0+y1*np.exp(-(2*t/T21)**beta1)
    return y0+y1*np.exp(-(2*t/T21)**beta1)+y2*np.exp(-(2*t/T22)**beta2)

def Mt2(t,Mtau,Mz0,M0,T21,T22,beta1,beta2):
    return (Mtau+(Mz0-Mtau)*np.exp(-(t/T21)**beta1))*np.exp(-(t/T22)**beta2)+M0

colors = iter(cm.jet(np.linspace(0, 1, 7)))
markers = iter([".","d","2","x","8","4","s","*","D","+","o","x","3","p"])

def T2(path,ax,temp,f,f2):
    time, amplitude, error = np.loadtxt(path, usecols=(0,5,6), unpack=True, comments='#')
    #var, cov = optimize.curve_fit(Mt2, time, amplitude, p0=(1e5,1e4,-1,1e-6,1e-8,-2,0.1), maxfev=1000000)
    time=np.append(time,5e-6)
    amplitude=np.append(amplitude,amplitude[0]*1.45)
    var, cov = optimize.curve_fit(Mt1, time, amplitude, p0=(-2,1000,4000,2.6e-5,2.4e-4,4e-2,1.7), maxfev=1000000)

    xRef = np.logspace(-5,-1,num=1000)
    yRef = Mt1(xRef, var[0],var[1],var[2],var[3],var[4],var[5],var[6])

    col=next(colors)
    mark = next(markers)

    plt.plot(xRef, yRef, color=col)
    plt.scatter(time,amplitude, color=col, marker=mark, label=temp+"K")
    plt.xscale("log")
    plt.xlim((5.5e-6,1e-3))
    plt.ylim((-100,6e3))

    f.write(temp+"\t"+str(var[3])+"\t"+str(np.sqrt(cov[3,3]))+"\t"+str(var[4])+"\t"+str(np.sqrt(cov[4,4]))+"\n")
    tempString = temp+" & "+str(round(var[3]*1e6,2))+" \\pm "+str(round(np.sqrt(cov[3,3])*1e6,2))+" & "+str(round(var[4]*1e4,2))+" \\pm "+str(round(np.sqrt(cov[4,4])*1e4,2))+" & "+str(round(var[5],2))+" \\pm "+str(round(np.sqrt(cov[5,5]),3))+" & "+str(round(var[6],2))+" \\pm "+str(round(np.sqrt(cov[6,6]),3))+" \\\\\\hline\n"
    f2.write(tempString)



path='../_daten/tieftemperatur/'
filelist = list()


figT2 = plt.figure()
axT2 = plt.gca()
axT2.set_xscale('log')



fOut=open("T2_data","w")
fOut.write("#Temp\ttauC\tstd\n")
fOut2=open("T2_data_latex","w")
fOut2.write("\\text{Temperatur } [K] & T_{21}\ [10^{-6}\ s] & T_{22}\ [10^{-4}\ s] & \\beta_1 & \\beta_2 \\\\\\hline\n")

for root, dirs, files in os.walk(path):
    options = root.split(sep="_")
    if len(options)>3:
        typ = options[3]
        temperature = options[4][:-1]
        if(typ=="T2"):
            temperature = round(float(temperature) * 0.922 - 1.085)
            for f in files:
                if(f.endswith(".nmr")):
                    filelist.append((temperature,root+"/"+f))

filelist = sorted(filelist,key=lambda x: x[0])
for temperature, filePath in filelist:
    T2(filePath,axT2,str(temperature),fOut,fOut2)


fOut.close()
fOut2.close()

plt.grid()
plt.legend()
#plt.ylim((-100,1000))
plt.title(r"$T_2$ Tieftemperatur Messwerte")
plt.xlabel("Zeit [s]")
plt.ylabel("Echo Amplitude")
plt.savefig("T2_tiefTemperaturFit.pdf")
