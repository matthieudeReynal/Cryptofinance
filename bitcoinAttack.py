# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 19:20:15 2020

@author: mattd
"""
import math
import numpy as np
import matplotlib.pyplot as plt
import random

alpha = 1.0/600
A = 5
t = 10
#k = 5
#q = 0.2
#p = 1 - q
n = 100
B = 6.25
#z = 3
v = 1.8


def Q(z,lambd):
    q = 0.0
    for k in range(z):
        q += lambd**k/math.factorial(k)*math.exp(-lambd)
    return q


def P(q, z, k):
    p = 1 - q
    pzk = 1 - Q(z, k*z*q/p) + (q/p)**z * math.exp(k*z*(p-q)/p) * Q(z, k*z)
    return pzk

def doubleSpend(q, z, k):
    cycle = 0
    dureeAttaque = 1
    gainAttaquant = 0
    while cycle < n:
        
        retard = 0
        zsim = z
        while(retard <= A):
            probaAttack = P(q, zsim,k)
            #print(probaAttack)
            probaHonnest = 1 - probaAttack
            aList = [0, 1]
            distribution = [probaHonnest, probaAttack]
            attackSuccess = random.choices(aList, distribution)
            #print(attackSuccess)
            if (attackSuccess[0] == 1 and retard ==0):
                gainAttaquant += (v+k*B)
                break
            if(attackSuccess[0] == 1 and retard !=0):
                retard -= 1
            else :
                retard += 1
                zsim += 1
            dureeAttaque += 1
        cycle += 1
    return [gainAttaquant, dureeAttaque]

#print(doubleSpe[d(6,2))
z = 6
k = 4.0
def honnestMining(q):
    duree = doubleSpend(q, z, k)[1]
    #print(duree)
    return (q/duree*B*n)

hashrate = []
DoubleSpend = []
HonnestMining = []
for i in range(100):
    hashrate.append(i/200.0)
    DoubleSpend.append(doubleSpend(hashrate[i], z, k)[0]/doubleSpend(hashrate[i], z, k)[1])
    HonnestMining.append(honnestMining(hashrate[i]))

#%matplotlib qt
#plt.figure()
    plt.clf()
plt.plot(hashrate, DoubleSpend, 'r') 
plt.plot(hashrate, HonnestMining, 'b')
#plt.figure()
plt.show()

B = 6.25
t0 = 10
q = 0.3
p = 1- q 
alphas = q/t0
alphah = p/t0
n0 = 2016
tau0 = 1/(alphas+alphah)
gamma = 0.3
    
def PSelfish(q, gamma):
    proba = q*B/tau0 - (1-gamma)*p**2*q*(p-q)*B/((1+p*q)*(p-q)+p*q)/tau0
    return proba
    
def PHonnest(q):
    proba = q*B/tau0
    return proba

def SelfishMining(q, gamma):
    cycle = 0
    dureeAttaque = 1
    gainAttaquant = 0
    while(cycle < n):
        avance = 0
        nbBlocs = 0
        while True:
            print(cycle)    
            nb2016BlocksMined = nbBlocs % 2016
            difficultyAdjustement = (p-q+p*q*(p-q)+p*q) * B / (p**2*q+p-q) / t0
            probaSelfish = PSelfish(q, gamma) * difficultyAdjustement**nb2016BlocksMined
            probaHonnest = 1 - probaSelfish
            aList = [0, 1]
            distribution = [probaHonnest, probaSelfish]
            attackSuccess = random.choices(aList, distribution)
            #print(distribution)
            if avance == 1 and attackSuccess[0] == 0:
                gainAttaquant += B * gamma
                dureeAttaque += 1
                break
            if avance == 2 and attackSuccess[0] == 0:
                gainAttaquant += 2 * B
                dureeAttaque += 1
                break
            if avance > 2 and attackSuccess[0] == 0:
                avance = 2
            if attackSuccess[0] == 1:
                avance += 1
            dureeAttaque += 1
            nbBlocs += 1
        cycle += 1
    return[gainAttaquant, dureeAttaque]

def honnestMining2(q):
    duree = SelfishMining(q, gamma)[1]
    #print(duree)
    return (q/duree*B*n)

#print(SelfishMining(0.4, 0.7))
#plt.figure()
plt.show()
"""
result = []
hashrate = []
selfishMining = []
HonnestMining = []
for i in range(20,100):
    hashrate.append(i/200.0)
    result.append(SelfishMining(hashrate[i-20], gamma))
    selfishMining.append(result[i-20][0]/result[i-20][1]*B*n)
    HonnestMining.append(result[i-20][1])

#%matplotlib qt
#plt.figure()
plt.clf()
plt.plot(hashrate, selfishMining, 'r') 
plt.plot(hashrate, HonnestMining, 'b') 
"""