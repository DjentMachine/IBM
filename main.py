###
# Main file for class and object testing. Calls the model with x interactions
# will eventually be the main class of our project
#
# Version 0.1
# Author: Diogo Barros
#

from classes import *
import numpy as np
import matplotlib.pyplot as plt
import statistics
from matplotlib import *

#Set variables for the archipelago
nIslands = 3
mLRichness = 1000
years = 1000
mainLand = []
for i in range(mLRichness):
    mainLand.append(1)

#Creating a test chained archipelago:
a = chainedArchipelago(mainLand, nIslands, mLRichness)
a.toString()
a.aUpdate(years)
a.toString()

print("First island mean:")
print(statistics.mean(a.timeRichness[0]))
print("Loop:")
for i in range(3):
    print(statistics.mean(a.timeRichness[i]))

#Visualizing data:
#t=plt.scatter(list(range(0,years)), a.timeRichness[0])
#plt.show()



#TO DO:
#Chained archipelago: equilibrium is the same?
#To read John Harte



    #Hav80952
