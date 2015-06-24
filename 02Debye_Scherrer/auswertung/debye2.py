#!/usr/bin/env python3

import numpy as np
import matplotlib.pylab as plt
import matplotlib as mpl

def sortArrayUpways(arr):
	n = len(arr)
	for i in range(0,n):
		for j in range(0,n):
			if(arr[i]<arr[j]):
				temp = arr[j]
				arr[j] = arr[i]
				arr[i] = temp
#####parameter
R = 57.4
lamda = 1.5417e-7

#####messwerte
r1_mess = np.array([32.0,44.0,53.0, 65.0,81.0])

r21_mess = np.array([34.0,46.0,56.0,61.0,65.0,74.0,78.0])
r21_mess = np.pi*R-r21_mess #möglicherweise geshiftet um viertel Umfang
r22_mess = np.array([31.0,38.0,44.0,51.0,65.0,69.0,74.0])
r2_mess = np.concatenate([r21_mess, r22_mess])
sortArrayUpways(r2_mess)

#####s-theorie
h1 = np.array([2,2,3,3,3])
k1 = np.array([0,2,1,2,3])
l1 = np.array([0,0,0,1,2])
h2 = np.array([2,2,2,3,4,3,4,5,6,6,5,6])
k2 = np.array([0,1,2,1,0,3,2,3,0,2,4,2])
l2 = np.array([0,1,0,0,0,0,0,0,0,0,1,2])

#####Winkel
theta1 = r1_mess/(2*R)
theta1_0 = theta1[0]
theta2 = r2_mess/(2*R)
theta2_0 = theta2[0]
#print("theta", theta2)
#####Strukturfaktoren
s_exp1 = 4*(np.sin(theta1))**2/(np.sin(theta1_0))**2
s_theo1 = h1**2 + k1**2 + l1**2
s_exp2 = 4*(np.sin(theta2))**2/(np.sin(theta2_0))**2
s_theo2 = h2**2 + k2**2 + l2**2

#a = np.sqrt(s_exp)*lamda/np.sin(theta1)


print("s_exp1: ",s_exp1)
print("s_theo1: ",s_theo1)
print("s_exp2: ", s_exp2)
print("s_theo2: ",s_theo2)

##test
t = np.linspace(1,4,100)
s = np.sin(t)**2/np.sin(t[0])**2


fig = plt.figure()
ax = plt.gca()
ax.scatter(t, s)
#plt.show()

