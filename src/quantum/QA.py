"""
This file is a lightly modified version of file from the
GPS: A new TSP formulation for its generalizations type QUBO article.

Original file can be found in this repository:
https://github.com/pifparfait/GPS

Author: Parfait Atchadé
"""

# https://arxiv.org/abs/2110.12158v3

import dwave.inspector
import qubovert
import dwave.system
import neal
import numpy as np
import matplotlib.pyplot as plt
from time import time

N = 7

M=N+1 # Number of points

# Generating points
puntos = np.random.rand(M,2)
for i in range(M):
    ang = 2*i*np.pi/M
    puntos[i,0],puntos[i,1] = np.cos(ang),np.sin(ang)
# print(puntos)
plt.plot(puntos[:,0],puntos[:,1],'o')

def fnorm(v):  ## v must be a np.array
    return np.sqrt(np.sum(v**2))

# Calculating distances
dist = np.zeros((N+2,N+2))
for i in range(N):
    for j in range(i+1,N+1):
        aux  =  fnorm(puntos[i,:]-puntos[j,:])
        dist[i,j],dist[j,i] = aux,aux

for j in range(0,N+1):
    i = N+1
    aux  =  fnorm(puntos[0,:]-puntos[j,:])
    dist[i,j],dist[j,i] = aux,aux

# Closest neighbour algorithm starting from 0
start_time = time()
lis_n = range(N+2)
dist_aux  = np.copy(dist)
for i in lis_n:
    dist_aux[i,i] = np.inf
dist_aux = np.copy(dist_aux[:-1,:-1])

i = 0
dist_vc = 0
ord_vc = [i]
for jj in range(N+1):
    dist_aux[jj,0] = np.inf

for cont in range(N):
    sig_dist = np.min(dist_aux[i,:])
    dist_vc += sig_dist
    sig = np.where(dist_aux[i,:] == sig_dist)[0][0]
    for jj in range(N+1):
        dist_aux[jj,sig] = np.inf
    i = sig
    ord_vc.append(i)

dist_vc += dist[ord_vc[-1],0]
ord_vc.append(0)

## We paint the proposed path
plt.plot(puntos[:,0],puntos[:,1],'o')
for i in range(len(ord_vc)-1):
        plt.plot(puntos[(ord_vc[i],ord_vc[i+1]),0],puntos[(ord_vc[i],ord_vc[i+1]),1])
plt.show()
elapsed_time = np.round(time()-start_time,3)
print("The time taken has been ",elapsed_time,"seconds.")

print("The order by nearest neighbors is ", ord_vc)
print("Length of the path", dist_vc)

modelo = 1 ## Poner 0 para SA, 1 para simulated QA, 2 para real QA
n_samples = 4000 # número de veces que ejecutamos el sistema

stm2 = time()

R=3
lis_r = range(R)
lis_n = range(0,N+2)

pen = 2
pen1 = 4

# We create the variables of our model
coef = qubovert.QUBO()

## Variables x_{i,j,r,q}
for i in lis_n:
    for j in lis_n:
        if not i==j:
            for r in lis_r:
                coef.create_var(f"x_{i}_{j}_{r}")
nqm2 = len(lis_n)*len(lis_n)*len(lis_r)
nqm2 = (N+2)*(N+2)*3

## Restricción 1
## Un solo caso para cada r
lambda_1 = dist_vc*pen
for i in lis_n:
    for j in lis_n:
        if not i==j:
            for r1 in lis_r:
                for r2 in lis_r:
                    coef[(f"x_{i}_{j}_{r1}",f"x_{i}_{j}_{r2}")] += (lambda_1)
            for r in lis_r:     
                    coef[(f"x_{i}_{j}_{r}",)] += -2*(lambda_1)



## Restriccion 2
## Se debe salir una vez de cada nodo
for i in range(N+1):
    lambda_2 = pen1*np.max(dist[i,])
    for j in lis_n:
        if not i == j:
            coef[(f"x_{i}_{j}_{1}",)] += -2*lambda_2 
    for j1 in  lis_n:
        if j1 != i:
            for j2 in lis_n:
                if j2!=i:
                    coef[(f"x_{i}_{j1}_{1}",f"x_{i}_{j2}_{1}")]+= lambda_2 



## Restriccion 3
## Se debe llegar una vez a cada nodo
for j in range(1,N+2):
    lambda_3 = np.max(dist[:,j])*pen1
    for i in range(N+1):
        if i!=j:
            coef[(f"x_{i}_{j}_{1}",)] += -2*lambda_3
    for i1 in  lis_n:
        if i1!=j:
            for i2 in lis_n:
                if i2!=j:
                    coef[(f"x_{i1}_{j}_{1}",f"x_{i2}_{j}_{1}")]+= lambda_3 


## Restriccion 7
## Correcto orden de los nodos i,j
lambda_7 = dist_vc*pen
for i in lis_n:
    for j in lis_n:
        if i!=j:
            coef[(f"x_{i}_{j}_{2}",f"x_{j}_{i}_{2}")] += lambda_7 
            coef[(f"x_{i}_{j}_{2}",)] += -lambda_7 
            coef[(f"x_{j}_{i}_{2}",)] += -lambda_7 





## Restriccion 8
## Relacion de orden entre los nodos i,j,k
lambda_8 = dist_vc*pen
for i in range(1,N+1):
    for j in range(1,N+1):
        for k in range(1,N+1):
            if i!=j and j!=k and i!=k:
                        coef[(f"x_{j}_{i}_{2}",f"x_{k}_{j}_{2}")] += lambda_8
                        coef[(f"x_{j}_{i}_{2}",f"x_{k}_{i}_{2}")] -= lambda_8
                        coef[(f"x_{k}_{j}_{2}",f"x_{k}_{i}_{2}")] -= lambda_8
                        coef[(f"x_{k}_{i}_{2}",)] +=  lambda_8


## Funcion objetivo
lambda_obj = 1
for i in lis_n:
    for j in lis_n:
        if i!=j:
            coef[(f"x_{i}_{j}_{1}",)] += lambda_obj*dist[i,j]

dwave_dic = {}
for i in coef:
    if len(i) == 1:
        dwave_dic[(i[0],i[0])] = coef[i]
    else:
        dwave_dic[i] = coef[i]

if modelo == 0:
    sampleset = qubovert.sim.anneal_qubo(dwave_dic, num_anneals=n_samples)
    solution = sampleset.best.state
        
if modelo == 1:
    sampler = neal.SimulatedAnnealingSampler()
    sampleset = sampler.sample_qubo(dwave_dic, num_reads = n_samples)
    solution = sampleset.first.sample
    
if modelo == 2:
    sampler = dwave.system.EmbeddingComposite(dwave.system.DWaveSampler())
    sampleset = sampler.sample_qubo(dwave_dic,num_reads = n_samples)
    solution = sampleset.first.sample

if modelo == 3:
    sampler = dwave.system.LeapHybridBQMSampler()
    sampleset = sampler.sample_qubo(dwave_dic)
    solution = sampleset.first.sample

print()
print("The number of qubits is",nqm2)

## Mejor energia
#print(sampleset.first.energy)
## Matriz solucion
mat_sol = np.zeros((N+2,N+2))
for i in  range(N+2):
    for j in range(N+2):
        if i!=j:
            if solution[f"x_{i}_{j}_{1}"] == 1:
                mat_sol[i,j] = 1
#print(mat_sol)

## Pintamos el camino propuesto
print()
print("Solution path drawing.")
plt.plot(puntos[:,0],puntos[:,1],'o')
vaux = np.array(list(range(N+2)))
suma_ruta = 0
for i in range(N+1):
    sig_aux = mat_sol[i,:]==1
    if np.sum(sig_aux) > 0:
        sig = (int(vaux[sig_aux][0]))%(N+1)
        plt.plot(puntos[(i,sig),0],puntos[(i,sig),1])
        suma_ruta += np.floor(1000*fnorm(puntos[i,:]-puntos[sig,:]))
plt.show()

## Calculamos la distancia que se recorre
val_resobj = 0
for i in lis_n:
    for j in lis_n:
        if i!=j:
            val_resobj += solution[f"x_{i}_{j}_{1}"]*lambda_obj*dist[i,j]
print()
print("The length of the solution path is",val_resobj)
lpm2 = val_resobj

etm2 = np.round((time()-stm2)/60,3) ## Elapsed time model 1
print()
print("Running time has been",etm2,"minutes.")

# bqm = dimod.generators.ran_r(1, 20)
# sampler = neal.SimulatedAnnealingSampler()
# sampleset = sampler.sample(bqm, num_reads=100)
# print(sampleset)