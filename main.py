"""
Main file for class and object testing. Calls the model with x interactions
will eventually be the main class of our project

Version 0.1
Author: Diogo Barros
"""

"""
TO DO:
To read John Harte
Implement spatial auto-correlationn
"""


from classes import *
import matplotlib.pyplot as plt
import statistics
#from matplotlib import *
import numpy as np

#Set variables for the archipelago
nIslands = 3
sppCapacity = 1000
initRichness = 100
years = 1000
pStart = int(years/2)
pEnd = years

#Creating a test chained archipelago:
a = chainedArchipelago(sppCapacity,nIslands,initRichness)
a.aUpdate(years)

#Statistics and data visualization:
print("Initial richness for all islands:")
for i in range(nIslands):
    print("Island %d : %d" % (i, a.timeRichness[i][0]))

print("\nIsland mean richness between year %d and %d:" % (pStart,pEnd))
for i in range(nIslands):
    print("Island %d mean: %f" % (i, statistics.mean(a.gTimeRichness(i,pStart,pEnd))))

#Visualizing 1 island
t=plt.scatter(list(range(-1,years)), a.timeRichness[0])
plt.show()





#Simulating multiple archipelagos:

#Islands characteristics
#nIslands = 3
#sppCapacity = 100
#initRichness = 100
#years = 100

#Archipelagos characteristics:
#nrArchipelagos = 2
#archipelagos = [chainedArchipelago(sppCapacity,nIslands) for i in range(nrArchipelagos)]

#for i in range(nrArchipelagos):
#    archipelagos[i] = chainedArchipelago(sppCapacity, nIslands, initRichness)




#Hav80952
