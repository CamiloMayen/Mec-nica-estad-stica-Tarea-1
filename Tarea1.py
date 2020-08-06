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
#Ubica la ubicacion de ffmpeg, que es la 'biblioteca' para poder sacar los videos.
plt.rcParams['animation.ffmpeg_path'] = '/usr/local/bin/ffmpeg'
#Este def solo le da vuelta a la lista
def regreson(y):
    y=y[::-1]
    return y
#Este def llena las listas para la posicion x & y de cada particula.
def lim(v,n,m):
    t=0
    y=[]
    if v>0:#Si la velocidad de la particula es positiva empieza desde la izquierda o desde abajo
        y.append(n-0.01)
        while y[-1]<=m:
            t+=0.05
            y.append(n+v*t)
    if v<0:#Si la velocidad de la particula es negativa empieza desde la derecha o desde arriba
        y.append(m+0.01)
        while y[-1]>=n:
            t+=0.05
            y.append(m+v*t)
    return y
ancho=2#Realmente el ancho de la caja es dos veces este numero.
alto=1#Realmente el alto de la caja es dos veces este numero.
N=100#Cantidad de particulas dentro de la caja
v=1#velocidad dada para todas las particulas
#De aqui en adelante se inicializan las listas que se van a emplear
thetas=[]#Para los angulos iniciales aleatorios para cada particula
Vx=[]#para la velocidad en x para cada particula
Vy=[]#para la velocidad en y para cada particula
Xs1=[]#posiciones en x para cada particula solo para la mitad de la caja de izquierda a derecha
Xs2=[]#posiciones en x para cada particula para toda la caja de izuierda a derecha
Ys=[]#posiciones en y para cada particula de abajo para arriba
Xr=[]#posiciones en x para cada particula para toda la caja de derecha a izquierda
Xr2=[]#posiciones en x para cada particula solo para la mitad de la caja de derecha a izquierda
Yr=[]#poscioens en y para cada particula de arriba para abajo
contx=[]#Indicara la posicion en x de cada particula 
conty=[]#Indicara la posicion en y de cada particula
vueltax=[]#Indicara si una particula va de derecha a izquierda o al revez
vueltay=[]#Inicara si una particlua va de arriba para abajo o al revez
XX=[]#Solo se una vez para la transicion de la mitad de la caja a toda la caja. Guarda la ultima lista de todas las partiuclas en x
YY=[]#Solo se una vez para la transicion de la mitad de la caja a toda la caja. Guarda la ultima lista de todas las partiuclas en y
Num=[]#guarda la cantidad de particulas que hay del lado derecho de la caja en todo momento. Es el eje y de la segunda grafica, de las iteraciones vs el tiempo
Num1=[]#guarda la cantidad de particulas que hay del lado derecho cuando solo estan de un lado de la caja. Es para el histograma de la tercera grafica
Num2=[]#guarda la cantidad de partiulas que hay del lado derecho cuando se abre la caja. Es para el histograma de la tercera grafica
#Se llena la lista de los angulos aleatorios
for i in range(N+1):
    thetas.append(rd.uniform(0,2*np.pi))
#Se llenan las lista de las velocidades en x & y
for i in thetas:
    Vx.append(v*np.cos(i))
    Vy.append(v*np.sin(i))
#Se llenan las listas para las posiciones de x (de toda la caja) & y usando lim definido al principio
for i in Vx:
    Xs1.append(lim(i,-ancho,ancho))
for i in Vy:
    Ys.append(lim(i,-alto,alto))
#Se llenan las listas para el regreso en x para toda la caja, las posiciones iniciales y la lista que decide en que direccion se dirige se llena de numero '2'
for i in Xs1:
    Xr.append(regreson(i))
    contx.append(int(len(i)/4))
    vueltax.append(2)
#Se llenan las listas para el regreso en y, las posiciones inciales y la lista que decide en que direccion se dirige de numero '2'
for i in Ys:
    Yr.append(regreson(i))
    conty.append(int(len(i)/2))
    vueltay.append(2)
#Se toma de la lista Xs1, que tiene las posiciones en x de cada particula en toda la caja, las posiciones del tope izquierdo hasta la mitad
for i in Xs1:
    temporal=[]
    for j in i:
        if j>(-ancho) and j<=(0):
            temporal.append(j)
    Xs2.append(temporal)
#Se hace la lista de regreso para la lista recien llenada
for i in Xs2:
    Xr2.append(regreson(i))
t=[0]#Aqui se guardan las itereaciones realizadas. Es el contador de iteraciones
unico=0#Solo se usa una vez al momento de pasar de la mitad a la caja a toda la caja
fig=plt.figure()#Se inicializa la figura para las graficas
camera = Camera(fig)#Se inicializa el objeto que toma las capturas de pantalla.
primero=False#Indica hasta cuando se mantiene en solo la mitad de la caja. Cuando se convierte en True pasa a toda la caja
segundo=True#Indica hasta cuando se mantiene en toda la caja. Cuando pasa a False se mantiene ahi hasta que vuelve a ser True
Global=False#Indica hasta cuando hacer todas las iteraciones (hasta cuando se mantiene dentro del while). Cuando para a True termina el proceso y procede a hacer el video
cont_primero=0#Indica el equilibrio en la primera mitad de la caja. Si llega a ser igual a 80 entonces permite que primero=True y comienza el proceso en toda la caja
cont_segundo=0#Indica el equilibrio cuando estan en toda la caja. Si llega a 60 entonces hace que Global=True y termina el while
while Global==False:
    mitad=0#Este contador siempre empieza en cero. Nos indica la cantidad de pelotas que hay del lado derecho de la caja
    xtemp=[]#Las posiciones actuales de cada particula en x. Este es el que se grafica y muestra la primera grafica del video
    ytemp=[]#Las posiciones actuales de cada particula en y. Este es el que se grafica y muestra la primera grafica del video.
    if primero==False:#Hasta que primero=True termina este ciclo. Este ciclo es para la  mitad de la caja
        for i in range(len(Xs1)):
            if vueltax[i]%2==0:#Si es un multiplo de 2, la particula va hacia la derecha y hace un copy de Xs2
                actualx=Xs2[i].copy()
            if vueltay[i]%2==0:#Si es multiplico de 2, la particula va hacia arriba y hace un copy de Ys
                actualy=Ys[i].copy()
            if vueltax[i]%2!=0:#Si es un numero impar, la particula va hacia la izquieda y hace un copy Xr2
                actualx=Xr2[i].copy()
            if vueltay[i]%2!=0:#Si es impar la particula va hacia abajo
                actualy=Yr[i].copy()
            xtemp.append(actualx[contx[i]])#Introduce la posicion en x de cada particula
            ytemp.append(actualy[conty[i]])#Introduce la posicion en y de cada particula
            if actualx[contx[i]]> -1:
                mitad+=1#Si una particula esta despues de la mitad la agrega al contador
            if contx[i]==(len(Xs2[i])-2):#Verifica si la particula llego hasta el una pared. De ser asi resetea el contador de posicion e indica que ahora va para el otro lado
                contx[i]=0
                vueltax[i]+=1
            if conty[i]==(len(Ys[i])-2):#Verifica si la particula llego hasta el una pared. De ser asi resetea el contador de posicion e indica que ahora va para el otro lado
                conty[i]=0
                vueltay[i]+=1
            contx[i]+=1#Le suma a la posicion en x
            conty[i]+=1#Le suma a la posicion en y
        if 45<mitad<55:#Si las particulas estan entre 45 y 55 cont_primero suma 1. De lo contrario se resetea. El objetivo es que cont_primero llegue hasta 80 de manera continua
            cont_primero+=1
        else:
            cont_primero=0
    if segundo==False:#Cuando cont_primero llega a 80 de manera continua segundo=False y empieza en este ciclo
        if unico==0:#Este if solo lo hace cuando entra por primera vez a este ciclo. Dado que las posiciones en las listas pequeñas en x no coinciden con las grandes, aqui se arregla eso
            for i in range(len(Xs1)):#Los ifs buscan en que direccion se dirige
                if vueltax[i]%2==0:
                    la_lista=XX[-1]#obtiene las ultimas posiciones graficadas
                    nuevo=Xs1[i].index(la_lista[i])#obtiene la posicion en la lista de x para toda la caja, de la ultima posicion graficada
                    contx[i]=nuevo+1#Se arregla su posicion en las listas grandes.
                if vueltax[i]%2!=0:
                    la_lista=XX[-1]
                    nuevo=Xr[i].index(la_lista[i])
                    contx[i]=nuevo+1
            unico+=1
        for i in range(len(Xs1)):#Este proceso es igual al anterior, solo que con Xs1 en lugar de Xs2
            if vueltax[i]%2==0:
                actualx=Xs1[i].copy()
            if vueltay[i]%2==0:
                actualy=Ys[i].copy()
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
            if conty[i]==(len(Ys[i])-2):
                conty[i]=0
                vueltay[i]+=1
            contx[i]+=1
            conty[i]+=1
        if 45<mitad<55:
            cont_segundo+=1
        else:
            cont_segundo=0
    Num.append(mitad)#Esta lista es la que va en el eje y de la segunda grafica en el video. Son las fluctuaciones de las particulas alrededor de la mitad
    if primero==False:    #Este if y el siguiente son para diferenciar los histogramas de equilibrio solo para la mitad de la caja o para l acaja completa
        Num1.append(mitad)
    if segundo==False:
        Num2.append(mitad)
    plt.subplot(311)#Se crea la grafica con las 3 sub-graficas. 311 quiere decir, de aqui en adelante grafica solo en la primra grafica de 3
    plt.xlim(-2,2)#limites en x
    plt.ylim(-1,1)#limites en y
    plt.xticks(visible=False)#Esta linea y la siguiente le quita los numeros a los ejes de la primera grafica, la que muestra la simulacion
    plt.yticks(visible=False)
    plt.plot(xtemp, ytemp, 'ob')#Grafica los puntos actuales de cada particula
    plt.subplot(312)#Aqui empieza a graficar en la segunda grafica, que muestra las fluctuaciones repecto las iteraciones
    plt.ylim(0,N)#limite en y, ya que son 100 particulas. Solo es por estetica, para que se mire que fluctua alrededor de la mitad
    plt.plot(t, Num,'-r')#Grafica las fluctuaciones respecto a las iteraciones
    if primero==False:    #Si esta solo en la mitad grafica en el histograma Num1. Esto para que cuando pasa a toda la caja las fluctuaciones no se mezclen, si no que sean individuales
        Num1.append(mitad)
        plt.subplot(313)
        plt.hist(Num1, bins=11, histtype='bar', ec='black',color='blue')
    if segundo==False:
        Num2.append(mitad)#Si esta en toda la caja el histograma lo saca de Num2.
        plt.subplot(313)
        plt.hist(Num2, bins=15, histtype='bar', ec='black',color='blue')
    camera.snap()#Este toma un screenshot de cada grafica realizada y la guarda. El total de screenshots obtenidos es igual a las iteraciones realizadas
    t.append(t[-1]+1)
    if cont_primero==80:#Este if es la transicion de estar solo en la mitad de la caj a a pasar a toda la caja. Cuando cont_primero=80 cambia a toda la caja cambiando el boolean de primero y segundo
        primero=True
        segundo=False
        XX.append(xtemp)
        YY.append(ytemp)
    if cont_segundo==60:#Cuando cont_segundo=60 termina el ciclo.
        Global=True
print("Proceso terminado")#Solo para poder diferenciar entre cuando realiza todas las graficas y cuando empieza a realizar el video
Writer = FuncAnimation.writers['ffmpeg']#Describe que es un video el que se va a hacer
writer = Writer(fps=90, metadata=dict(artist='Me'), bitrate=1800)#Se describen las caracterisitcas del video
animation = camera.animate()  #Aqui se realiza el video con las descripciones anteriores.
animation.save('Prueba 5.1.mp4', writer = writer)#Guarda el video
