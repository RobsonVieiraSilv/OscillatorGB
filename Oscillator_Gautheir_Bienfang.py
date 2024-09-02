#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 17:04:16 2024

@author: robson
"""

import numpy as np
import matplotlib.pyplot as plt

#%%

### equações do circuito
def Sys_MS(r, kp, rm, p):
    
    V1s = r[0]
    V2s = r[1]
    Is = r[2]
    

    
    # Parâmetros do circuito
    R1, R2, R3 = p
    kp1, kp2, kp3 = kp
    V1m, V2m, Im = rm

    dV1 = (V1s/R1) - g(V1s - V2s, R2) + cd*kp1*(V1m - V1s)
    dV2 = g(V1s - V2s, R2) - Is   +  cd*kp2*(V2m - V2s)
    dI = V2s - (R3 * Is) + cd*kp3*(Im - Is)

    return np.array([dV1, dV2, dI])


### Equação do elemento não linear
def g(V, R2):

    Ir = 22.4E-6
    a = 11.34

    return 2.0*Ir*np.sinh(a*V) + V/R2


# Runge_kutta 4th order
def rk4(r, rm = [0.0, 0.0, 0.0], kp = [0.0, 0.0, 0.0], p0 = [1.30, 3.44, 0.193]):

    
    
#    rm = [V1m, V2m, Im]

    k1 = dt*Sys_MS(r, kp, rm, p0)
    k2 = dt*Sys_MS(r + k1/2.0, kp, rm, p0)
    k3 = dt*Sys_MS(r + k2/2.0, kp, rm, p0)
    k4 = dt*Sys_MS(r + k3, kp, rm, p0)
    
    
    return r + (k1 + 2.0 * k2 + 2.0 * k3 + k4)/6.0

#%%

# Número de pontos e passo de evolução temporal
N_hist = 5
N = 10000
dt = 0.1
t = np.arange(0, N*dt, dt)

# Condiçoes iniciais circuito mestre
rm = np.zeros((3, N))
rs = np.zeros((3, N))

# As condições devem ser diferentes
rm[:, 0] = [0.0, 0.1, 0.0]
rs[:, 0] = [0.0, 0.0, 1.0]

### matrix do acoplamento 
kp0 = [1.0, 0.0, 0.0]

# parâmetros do sistema (valores dos resistores: R1, R2, R3)
p = [1.313, 3.4744, 0.195]

### parâmetro do acoplamento 
cd = 0

#%%

### Determina a evolução do sistema ######
for i in range(N_hist):
    
    for n in range(N - 1):
        
        # Sistema mestre
        rm[:, n + 1] = rk4(rm[:, n])
        
        # Sistema escrvavo
        # Acoplamento com V1s e V1m
        rs[:, n + 1]  = rk4(rs[:, n], rm = rm[:, n + 1], kp = kp0, p0 = p) 
    
    rm[:, 0] = rm[:, -1]
    rs[:, 0] = rs[:, -1]

#%%
V1m = rm[0, :]    
V2m  = rm[1, :]
Im = rm[2, :]

V1s = rs[0, :]    
V2s  = rs[1, :]
Is = rs[2, :]

#%%
######## PLotando os gráficos #####################

plt.figure(0, figsize=(15,8))
plt.subplot(221)
plt.plot(t, V1m)
plt.plot(t, V2m)
plt.xlabel("t", fontsize=15)
plt.ylabel("$V_{1m}$; $V_{2m}$", fontsize=15)
plt.subplot(222)
plt.plot(V1m, V2m)
plt.xlabel("$V_{1m}$", fontsize=15)
plt.ylabel("$V_{2m}$", fontsize=15)
plt.subplot(223)
plt.plot(t, V1s)
plt.plot(t, V2s)
plt.xlabel("t", fontsize=15)
plt.ylabel("$V_{1s}$; $V_{2s}$", fontsize=15)
plt.subplot(224)
plt.plot(V1s, V2s)
plt.xlabel("$V_{1s}$", fontsize=15)
plt.ylabel("$V_{2s}$", fontsize=15)


plt.figure(2, figsize=(15,5))
plt.subplot(121)
plt.plot(t, V2m)
plt.plot(t, V2s)
plt.xlabel("t", fontsize=15)
plt.ylabel("$V_{2m}$; $V_{2s}$", fontsize=15)
plt.subplot(122)
plt.plot(V1s, V1m)
plt.xlabel("$V_{2s}$", fontsize=15)
plt.ylabel("$V_{2m}$", fontsize=15)
