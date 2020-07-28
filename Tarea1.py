#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 19:47:26 2020

@author: Camilo Mayen
"""

import numpy as np
import matplotlib.animation as FuncAnimation
from celluloid import Camera
import matplotlib.pyplot as plt
import random as rd
plt.rcParams['animation.ffmpeg_path'] = '/usr/local/bin/ffmpeg'

def regreson(y):
    y=y[::-1]
    return y

def lim(v,n,m):
    t=0
    y=[]
    if v>0:    
        y.append(n-0.01)
        while y[-1]<=m:
            t+=0.05
            y.append(n+v*t)
    if v<0:
        y.append(m+0.01)
        while y[-1]>=n:
            t+=0.05
            y.append(m+v*t)
    return y


limite=800
ancho=2
alto=1
N=100
v=1
thetas=[]
Vx=[]
Vy=[]
Xs1=[]
Xs2=[]
Ys1=[]
Xr=[]
Xr2=[]
Yr=[]
contx=[]
conty=[]
vueltax=[]
vueltay=[]
XX=[]
YY=[]
Num=[]
Num1=[]
Num2=[]
for i in range(N+1):
    thetas.append(rd.uniform(0,2*np.pi))
for i in thetas:
    Vx.append(v*np.cos(i))
    Vy.append(v*np.sin(i))
for i in Vx:
    Xs1.append(lim(i,-ancho,ancho))
for i in Vy:
    Ys1.append(lim(i,-alto,alto))
for i in Xs1:
    Xr.append(regreson(i))
    contx.append(int(len(i)/4))
    vueltax.append(2)
for i in Ys1:
    Yr.append(regreson(i))
    conty.append(int(len(i)/2))
    vueltay.append(2)
for i in Xs1:
    temporal=[]
    for j in i:
        if j>(-ancho) and j<=(0):
            temporal.append(j)
    Xs2.append(temporal)
for i in Xs2:
    Xr2.append(regreson(i))


t=[0]
unico=0
fig=plt.figure()
camera = Camera(fig)
primero=False
segundo=True
Global=False
cont_primero=0
cont_segundo=0
while Global==False:
    mitad=0
    xtemp=[]
    ytemp=[]
    if primero==False:
        for i in range(len(Xs1)):
            if vueltax[i]%2==0:
                actualx=Xs2[i].copy()
            if vueltay[i]%2==0:
                actualy=Ys1[i].copy()
            if vueltax[i]%2!=0:
                actualx=Xr2[i].copy()
            if vueltay[i]%2!=0:
                actualy=Yr[i].copy()
            xtemp.append(actualx[contx[i]])
            ytemp.append(actualy[conty[i]])
            if actualx[contx[i]]> -1:
                mitad+=1
            if contx[i]==(len(Xs2[i])-2):
                contx[i]=0
                vueltax[i]+=1
            if conty[i]==(len(Ys1[i])-2):
                conty[i]=0
                vueltay[i]+=1
            contx[i]+=1
            conty[i]+=1
        if 45<mitad<55:
            cont_primero+=1
        else:
            cont_primero=0
    if segundo==False:
        if unico==0:
            for i in range(len(Xs1)):
                if vueltax[i]%2==0:
                    la_lista=XX[-1]
                    nuevo=Xs1[i].index(la_lista[i])
                    contx[i]=nuevo+1
                if vueltax[i]%2!=0:
                    la_lista=XX[-1]
                    nuevo=Xr[i].index(la_lista[i])
                    contx[i]=nuevo+1
            unico+=1
        for i in range(len(Xs1)):
            if vueltax[i]%2==0:
                actualx=Xs1[i].copy()
            if vueltay[i]%2==0:
                actualy=Ys1[i].copy()
            if vueltax[i]%2!=0:
                actualx=Xr[i].copy()
            if vueltay[i]%2!=0:
                actualy=Yr[i].copy()
            xtemp.append(actualx[contx[i]])
            ytemp.append(actualy[conty[i]])
            if actualx[contx[i]]>0:
                mitad+=1
            if contx[i]==(len(Xs1[i])-2):
                contx[i]=0
                vueltax[i]+=1
            if conty[i]==(len(Ys1[i])-2):
                conty[i]=0
                vueltay[i]+=1
            contx[i]+=1
            conty[i]+=1
        if 45<mitad<55:
            cont_segundo+=1
        else:
            cont_segundo=0
    Num.append(mitad)
    if primero==False:    
        Num1.append(mitad)
    if segundo==False:
        Num2.append(mitad)
    XX.append(xtemp)
    YY.append(ytemp)
    plt.subplot(311)
    plt.xlim(-2,2)
    plt.ylim(-1,1)
    plt.xticks(visible=False)
    plt.yticks(visible=False)
    plt.plot(xtemp, ytemp, 'ob')
    plt.subplot(312)
    plt.ylim(0,100)
    plt.plot(t, Num,'-r')
    if primero==False:    
        Num1.append(mitad)
        plt.subplot(313)
        plt.hist(Num1, bins=11, histtype='bar', ec='black',color='blue')
    if segundo==False:
        Num2.append(mitad)
        plt.subplot(313)
        plt.hist(Num2, bins=15, histtype='bar', ec='black',color='blue')
    camera.snap()
    t.append(t[-1]+1)
    if cont_primero==80:
        primero=True
        segundo=False
    if cont_segundo==50:
        Global=True
print("Proceso terminado")
Writer = FuncAnimation.writers['ffmpeg']
writer = Writer(fps=90, metadata=dict(artist='Me'), bitrate=1800)
animation = camera.animate()  
animation.save('Prueba 4.5.mp4', writer = writer)

