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
from matplotlib import *
import numpy as np

#Set variables for the archipelago
nIslands = 3
sppCapacity = 1000
initRichness = 100
years = 1000


#Creating a test chained archipelago:
a = chainedArchipelago(sppCapacity,nIslands,initRichness)
a.toString()
a.aUpdate(years)
a.toString()

#Statistics and data visualization:
#print("Island means:")
#for i in range(nIslands):
#    print(statistics.mean(a.timeRichness[i][int(len(a.timeRichness[i])/2):len(a.timeRichness[i])]))
#    print(a.coords[i])



#t=plt.scatter(list(range(-1,years)), a.timeRichness[0])
#plt.show()


#for i in range(a.islandNr):
#    print(sum(1 for x in a.islands[i].sourcePop if x == 1))
#    print(a.islands[i].sourcePop)
#    print(a.islands[i].gRichness())


    #Hav80952
