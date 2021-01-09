# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 19:20:15 2020

@author: mattd
"""
import math
#import numpy as np
import matplotlib.pyplot as plt
import random

alpha = 1.0/600
#A = 5
t = 10
#k = 5
#q = 0.2
#p = 1 - q
#n = 4570
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

def doubleSpend(q, z, k, A, n):
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
            """
            gainAttaquant+= (v+B)*probaAttack
            retard += q
            print(retard)
            """
        dureeAttaque += 1
        cycle += 1
    return [gainAttaquant, dureeAttaque]
#*10/6.25
#print(doubleSpend(0.3,6,2))
z = 6
k = 4.0
def honnestMining(q):
    duree = doubleSpend(q, z, k)[1]
    #print(duree)
    return (q/duree*B*n)

def simulateDoubleSpend(n, A, k, z):
    hashrate = []
    DoubleSpend = []
    HonnestMining = []
    result = []
    for i in range(20,100):
        print("computing ", i-20, "/80")
        hashrate.append(i/200.0)
        result.append(doubleSpend(hashrate[i-20],z,k,A,n))
        DoubleSpend.append(result[i-20][0]/result[i-20][1]/6.25)
        HonnestMining.append(i/200.0)
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
gamma = 0.77
    
def PSelfish(q, gamma):
    proba = q*B/tau0 - (1-gamma)*p**2*q*(p-q)*B/((1+p*q)*(p-q)+p*q)/tau0
    return proba
    
def PHonnest(q):
    proba = q*B/tau0
    return proba

difficultyAdjustement = (p-q+p*q*(p-q)+p*q) / (p**2*q+p-q)
def SelfishMining(q, gamma):
    
    cycle = 0
    dureeAttaque = 1
    gainAttaquant = 0
    nbBlocs = 0
    difficultyAdjustement = (p-q+p*q*(p-q)+p*q) / (p**2*q+p-q)
    while(cycle < n):
        avance = 0
        
        nb2016BlocksMined = nbBlocs // 2016
        
        while True:
            print(cycle)    
            #print(nb2016BlocksMined)
            #print(nbBlocs)
            #probaSelfish = PSelfish(q, gamma)# * difficultyAdjustement**nb2016BlocksMined
            probaSelfish = q* difficultyAdjustement**nb2016BlocksMined
            probaHonnest = (1 - probaSelfish)
            aList = [0, 1]
            distribution = [probaHonnest, probaSelfish]
            attackSuccess = random.choices(aList, distribution)
            print(distribution)
            """
            if avance == 1 and attackSuccess[0] == 0:
                bList = [0, 1]
                distribution2 = [gamma, 1- gamma]
                gammaSuccess = random.choices(bList, distribution2)
                if(gammaSuccess[0]==0):
                    gainAttaquant += B
                dureeAttaque += 1
                nbBlocs += 1
                break
            if avance == 2 and attackSuccess[0] == 0:
                gainAttaquant += 2 * B
                dureeAttaque += 1
                nbBlocs+=1
                break
            
            if avance == 2:
                gainAttaquant += 2 * B
                dureeAttaque += 2
                break
            
            if avance > 2 and attackSuccess[0] == 0:
                avance = 2
                gainAttaquant += B*(avance-2)
            if attackSuccess[0] == 1:
                avance += 1
            """
            if attackSuccess[0] == 1:
                avance += 1
                if avance == 2:
                    gainAttaquant += 2*B 
                    avance = 0
                    #dureeAttaque += 2
                    break
                
            if attackSuccess[0] == 0:
                nbBlocs += 1
                dureeAttaque += 1
                if avance == 0:
                    break
                if avance == 1:
                    bList = [0, 1]
                    distribution2 = [gamma, 1- gamma]
                    gammaSuccess = random.choices(bList, distribution2)
                    if(gammaSuccess[0]==0):
                        gainAttaquant += B
                    break
                if avance == 2:
                    gainAttaquant += 2*B
                    break
                else:
                    gainAttaquant += (avance-2)*B
                    avance = 2
                """
                dureeAttaque += 1
                nbBlocs += 1
                break
                """
            dureeAttaque += 1
            nbBlocs += 1
        cycle += 1
    return[gainAttaquant, dureeAttaque]

def honnestMining2(q):
    duree = SelfishMining(q, gamma)[1]
    #print(duree)
    return (q/duree*B*n)

result = SelfishMining(0.25, 0.77)
print(result[0]/result[1]/6.25)

def simulateSelfishMining(n, gamma):
    result = []
    hashrate = []
    selfishMining = []
    HonnestMining = []
    for i in range(20,100):
        hashrate.append(i/200.0)
        result.append(SelfishMining(hashrate[i-20], gamma))
        selfishMining.append(result[i-20][0]/result[i-20][1]/B)
        HonnestMining.append(hashrate[i-20])
    plt.clf()
    plt.plot(hashrate, selfishMining, 'r') 
    plt.plot(hashrate, HonnestMining, 'b')
    plt.show() 


def SelfishMiningBCash(q, gamma):
    
    cycle = 0
    dureeAttaque = 1
    gainAttaquant = 1
    
    
    while(cycle < n):
        avance = 0
        nbBlocs = 0
        nb144BlocksMined = nbBlocs // 144
        
        while True:
            print(cycle)
            difficultyAdjustementBCash = 144*600/(dureeAttaque%144+1)/600
            #print(nb2016BlocksMined)
            #print(nbBlocs)
            #probaSelfish = PSelfish(q, gamma)# * difficultyAdjustement**nb2016BlocksMined
            probaSelfish = q* difficultyAdjustementBCash**nbBlocs
            probaHonnest = (1 - probaSelfish)
            aList = [0, 1]
            distribution = [probaHonnest, probaSelfish]
            attackSuccess = random.choices(aList, distribution)
            print(distribution)
            """
            if avance == 1 and attackSuccess[0] == 0:
                bList = [0, 1]
                distribution2 = [gamma, 1- gamma]
                gammaSuccess = random.choices(bList, distribution2)
                if(gammaSuccess[0]==0):
                    gainAttaquant += B
                dureeAttaque += 1
                nbBlocs += 1
                break
            if avance == 2 and attackSuccess[0] == 0:
                gainAttaquant += 2 * B
                dureeAttaque += 1
                nbBlocs+=1
                break
            
            if avance == 2:
                gainAttaquant += 2 * B
                dureeAttaque += 2
                break
            
            if avance > 2 and attackSuccess[0] == 0:
                avance = 2
                gainAttaquant += B*(avance-2)
            if attackSuccess[0] == 1:
                avance += 1
            """
            if attackSuccess[0] == 1:
                avance += 1
                if avance == 2:
                    gainAttaquant += 2*B 
                    avance = 0
                    #dureeAttaque += 2
                    break
                
            if attackSuccess[0] == 0:
                nbBlocs += 1
                dureeAttaque += 1
                if avance == 0:
                    break
                if avance == 1:
                    bList = [0, 1]
                    distribution2 = [gamma, 1- gamma]
                    gammaSuccess = random.choices(bList, distribution2)
                    if(gammaSuccess[0]==0):
                        gainAttaquant += B
                    break
                if avance == 2:
                    gainAttaquant += 2*B
                    break
                else:
                    gainAttaquant += (avance-2)*B
                    avance = 2
                """
                dureeAttaque += 1
                nbBlocs += 1
                break
                """
            dureeAttaque += 1
            nbBlocs += 1
        cycle += 1
    return[gainAttaquant, dureeAttaque]
    
def simulateSelfishMiningBCash(n, gamma):
    plt.show()
    result = []
    hashrate = []
    selfishMining = []
    HonnestMining = []
    for i in range(20,100):
        hashrate.append(i/200.0)
        result.append(SelfishMiningBCash(hashrate[i-20], gamma))
        selfishMining.append(result[i-20][0]/result[i-20][1]/B)
        HonnestMining.append(hashrate[i-20])
    plt.plot(hashrate, selfishMining, 'r') 
    plt.plot(hashrate, HonnestMining, 'b') 

def menu():
    print("1 : double dépense")
    print("2 : minage égoïste Bitcoin")
    print("3 : minage égoïste BCash")
    print("4 : quitter")
    saisie = int(input("choisir une option : "))
    if saisie == 1:
        n = int(input("n = "))
        A = int(input("A = "))
        k = int(input("k = "))
        z = int(input("z = "))
        simulateDoubleSpend(n, A, k, z)
menu()
