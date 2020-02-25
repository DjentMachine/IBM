"""
Main file for class and object testing. Calls the model with x interactions
will eventually be the main class of our project

Version 0.9
Author: Diogo Barros
"""

##
# TODO: visualization of plots
# TODO: To read John Harte
##

import time
import os.path
import math
import statistics as st
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
from classes import *

#Set variables for the system: simulating multiple archipelagos:
archipelagoNr = 3
arches = []
islandNr = 10
sppCapacity = 1000
initRichness = 10
years = 1000
yearStart = int(years/2)
yearEnd = yearStart+100


#Start simulation and print information for archipelagos
startTime = time.time()
for i in range(archipelagoNr):
    arches.append(Archipelago(sppCapacity, islandNr, initRichness=initRichness, iWidth=0, aType="CWB"))
    arches[i].aUpdate(years)
    print("\n###ARCHIPELAGO %d ###" %(i+1))
    arches[i].toString()
    print("\nTime elapsed is {} seconds\n".format(time.time()-startTime))

if(islandNr<10):
    print("Richness in archipelagos at year %d:" % (yearStart))
    for i in range(archipelagoNr):
        print("\nArchipelago %d" %(i+1))
        for j in range(arches[i].islandNr):
            print("Island %d: %d" % (j+1, arches[i].gTimeRichness(yearStart, yearEnd + 1)[j]))

#Creating my dataframes
sars=[0]*len(arches)
scaz=pd.DataFrame([arches[0].speciesArea()])

for i in range(archipelagoNr):
    if i > 0:
        scaz=scaz.append(pd.DataFrame([arches[i].speciesArea()]), ignore_index=True)
    scaz.rename_axis("Arch nr")
    sars[i] = pd.DataFrame({
    "Archipelago":[i+1]*len(arches[i].iRichness),
    "Richness":arches[i].iRichness,
    "Area":arches[i].areas()
    })
print("\nSCAZ relationships for each archipelago:")
print(scaz)

data = pd.concat(sars)
data["Richness"]=data["Richness"].apply(math.log)
data["Area"]=data["Area"].apply(math.log)

timeRichness= pd.DataFrame({"Time": [i for i in range(years+1)]})
for z in range(len(arches)):
    for i in range(arches[z].islandNr):
        timeRichness["A{} - Island {}".format(i+1, z+1)] = arches[0].timeRichness[i]
"""
#Visualizing data: species growth throughout time in an archipelago
archipelago=0
rows = 2
cols = math.ceil(arches[0].islandNr/rows)
for i in range(arches[0].islandNr):
    plt.subplot(cols,rows,i+1)
    plt.scatter(list(range(years+1)), arches[archipelago].timeRichness[i])
    plt.title("Island %d" %(i+1))
plt.xlabel("Time")
plt.ylabel("Richness")
plt.suptitle("Richness over time in archipelago %d" %(archipelago+1),fontsize=20, weight=20)
"""
#Plotting coordinates of islands
"""
a = []
b = []
for i in range(len(arches[0].iCoords)):
    a.append(arches[0].iCoords[i][0])
    b.append(arches[0].iCoords[i][1])
a.append(arches[0].mainLand.coords[0])
b.append(arches[0].mainLand.coords[1])
plt.scatter(a,b)
plt.title("Island coordinates",fontsize=20, weight=20)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
"""

#Visualizing data: Species-Area relationship per Archipelago
#sns.lmplot(y="Richness", x="Area", col="Archipelago", data=data).fig.suptitle("Irate=e^(-d+A)")#, size=4,col_wrap=5)
#plt.subplots_adjust(top=0.85)
#Outputting data
#scaz.to_csv("/Users/diogobarros/Desktop/scaz.csv")
#data.to_csv("/Users/diogobarros/Desktop/sarLogData.csv")
#timeRichness.to_csv("/Users/diogobarros/Desktop/timeRichness.csv")


