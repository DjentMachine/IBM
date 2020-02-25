##
# Testing ground for SAR script
#
# v 0.2
# author: Diogo Barros
##

##
# TODO: Think about AMin possibility. Does it make sense for a user to set min and max values for area?
# TODO: understand why both math and sqrt are needed
# TODO: updat timeRichness in islands and archipelagos. Make one dependent of the other (IMPORTANT)
# TODO: set __str__ instead of creating a toString as in java
# TODO: Pass Update into Island class
##

import random
import statistics as st
from haversine import *
# import numpy as np
import pandas as pd
from scipy import stats
import math


class Island:
    def __init__(self, sppCapacity, isML=False, coordRange=[[32, 40], [-24,-32]], aMax=10000, initRichness = 1):
        """
        Constructor for the island class:
        sppCapacity: species capacity for the island
        isML: Is the island a main land?
        coordRange: ficticious WGS coordinates for the archipelago.
        Amax: maximum area value possible
        initRichness: initial number of species in the island
        """
        self.isML = isML
        self.area = random.randint(10, aMax)
        self.coords = [random.uniform(coordRange[0][0], coordRange[0][1]),
                       random.uniform(coordRange[1][0], coordRange[1][1])]
        if isML:
            self.sppCapacity = [1] * sppCapacity
            self.area = aMax
            self.coords = [coordRange[0][1]+1, coordRange[1][0]-1]
        else:
            self.sppCapacity = [0] * sppCapacity
        self.timeRichness = []
        self.iInitiate(initRichness)

    def iInitiate(self, initRichness):
        """
        Initiates the island with a given species richness sampled from a source
        :param initRichness: the chosen initial richness for the island
        :return: n/a
        """
        if not self.isML:
            for i in range(initRichness):
                r = random.randint(0, len(self.sppCapacity) - 1)
                self.sppCapacity[r] = 1
        self.timeRichness.append(self.gRichness())

    def migrate(self, sourceIsland):
        """
        A function that causes migration of 1 random species from one place to another with a given m probability.
        A species only migrates if it exists in Source Population and is not yet on the island
        !!!The smaller the ALPHA the larger the iRate!!!
        :param sourceIsland: island from which migrants come
        :return: possibly causes migration of 1 species
        """
        rM = random.uniform(0, 1)
        #alpha =  (self.distance(sourceIsland) - self.distance(sourceIsland)) /10000
        #alpha = math.e**(-self.distance(sourceIsland))*math.e**(self.area)  # TOO LARGE!
        #alpha = self.area*math.e**(-self.distance(sourceIsland))
        #alpha = self.distance(sourceIsland)/self.area
        #alpha = math.e**(-(self.distance(sourceIsland))/self.area)  # 0<=alpha<=1,larger == + likely migration occurs
        #iRate = 1 - (self.gRichness() / len(self.sppCapacity)) ** alpha  # IR=1-(S/ST)^alpha
        iRate = 1 - math.e**((-self.distance(sourceIsland)/(self.area/1000)))
        #iRate = 1 - math.e**((-1/(self.area/1000)))
        rPosition = random.randint(0, len(self.sppCapacity) - 1)
        if self.sppCapacity[rPosition] == 0 and \
                rM < iRate:  # A species migrates with probability m
            self.sppCapacity[rPosition] = 1

    def extinguish(self):
        """
        A function that causes extinction of 1 random species from one place to another with a given m probability
        :return:
        """
        rE = random.uniform(0, 1)
        gamma = random.uniform(0, 1)                                 # ??? meaning of this variable?
        beta = self.area/50                                          # Beta >= 1, =area/minArea
        eRate = gamma * (self.gRichness() / len(self.sppCapacity)) ** beta    # Er= gamma*(s/ST)^Beta, gamma >=1
        rPosition = random.randint(0, len(self.sppCapacity) - 1)
        if self.sppCapacity[rPosition] == 1 and rE < eRate:  # A species goes extinct  with probability e
            self.sppCapacity[rPosition] = 0

    def distance(self, sourceIsland):
        """
        Calculates distance between 2 islands
        :return:
        """
        return haversine(self.coords, sourceIsland.coords)

    def gRichness(self):
        """
        :return: total species richness for the island
        """

        return sum(1 for x in self.sppCapacity if x == 1)

    def gTimeRichness(self, minimum, maximum):
        """
        Returns the richness from a given island from a set interval of time
        :param minimum: minimum time
        :param maximum: maximum time
        :return: a vector with the time richness
        """
        return st.mean(self.timeRichness[minimum:maximum])

    """
    def isAtEquilivrium(self,island):
        equi = False
        if self.gTimeRichness(self.timeRichness[int(len(self.timeRichness)*0.1)],self.gRichness()) 
        < self.gRichness()-50:
            equi == True
        return equi
    """
    def toString(self):
        """
        To string method. Shouts a resume of the island atributes
        """
        print("This is a generated island with the following attributes:\n"
              "Area: %d m^2\nCurrent number of species: %d\nCurrent species on island: " %
              (self.area, self.gRichness()))
        print(self.sppCapacity)

##
# ARCHIPELAGO CLASS
##

class Archipelago:
    def __init__(self, sppCapacity, islandNr, initRichness=1, coordRange=[[39, 35], [-24,-27]], Amax=1000,
                 iWidth=2, aType="scattered"):
        """
        Constructor for the Archipelago class. An archipelago has x islands with different migration and
       extintion rates. They all assume the same Main Land.
        """
        self.islandNr = random.randint(islandNr - iWidth, islandNr + iWidth)
        self.islands = []
        self.mainLand = Island(sppCapacity, isML=True)
        self.iRichness = []
        self.timeRichness = [[] for _ in range(self.islandNr)]
        self.iCoords = []
        self.aType = aType
        for i in range(self.islandNr):
            self.islands.append(Island(sppCapacity, False, coordRange, Amax, initRichness))
            self.iRichness.append(self.islands[i].gRichness())
            self.timeRichness[i].append(self.iRichness[i])
            self.iCoords.append(self.islands[i].coords)
        if aType != "scattered": self.sortIslands()

    def aUpdate(self, years=1):
        """
        Updates archipelago with each interaction
        """
        for i in range(years):
            self.aMigrate()
            self.aExtinguish()
            for j in range(self.islandNr):
                self.iRichness[j] = self.islands[j].gRichness()
                self.timeRichness[j].append(self.islands[j].gRichness())

    def aMigrate(self):
        """
        Causes migration from 1 neighbouring island to a target island with a probability m
        """

        #Scattered migration
        if self.aType == "scattered":
            for i in range(self.islandNr):
                self.islands[i].migrate(self.mainLand)       # migrate from Main Land
                for j in range(self.islandNr):
                    if i != j:
                        self.islands[i].migrate(self.islands[j])
            self.iRichness[i] = self.islands[i].gRichness()
        #Chained migration
        elif self.aType == "chained":
            for i in range(self.islandNr):
                if i == 0:
                    self.islands[i].migrate(self.mainLand)       # migrate from Main Land
                else:
                    self.islands[i].migrate(self.islands[i-1])
        #Chained with benefits migration
        elif self.aType == "CWB":
            for i in range(self.islandNr):
                self.islands[i].migrate(self.mainLand)       # every island gets spp from Main Land
                for j in range(i):
                    self.islands[i].migrate(self.islands[j])


    def aExtinguish(self):
        """
        Extinguishes one species form an island in an archipelago with a probability e
        """
        for i in range(self.islandNr):
            self.islands[i].extinguish()

    def gTimeRichness(self, minimum, maximum):
        """
        Returns the richness from a given island from a set interval of time
        :param minimum: minimum time
        :param maximum: maximum time
        :return: a vector with the time richness
        """
        myList = []
        for i in range(self.islandNr):
            myList.append(st.mean(self.timeRichness[i][minimum:maximum]))
        return myList

    def areas(self):
        """
        Returns all island areas
        """
        a = []
        for i in range(self.islandNr):
            a.append(self.islands[i].area)
        return a

    def speciesArea(self):
        """
        :return: a list containing the values of slope, intercept, R^2 and P-value and std error of the species-area
        relationship
        """
        return stats.linregress(self.areas(), self.iRichness)

    def results(self):
        """
        :return: a Dataframe in which rows are islands and collumns are island atributes (area, and species)
        """
        return pd.DataFrame({"Richness": self.iRichness, "Area": self.areas()})

    def toString(self):
        """
        To string method. Shouts a resume of the archipelago's atributes
        """
        print("This is a generated archipelago with the following attributes:\n"
              "Nr of islands: %d" % self.islandNr)
        print("Area of the islands:")
        print(self.areas())
        print("Initial richness in the islands:")
        [print(self.timeRichness[i][0], end=" ") for i in range(self.islandNr)]
        print("\nActual richness in the islands:")
        print(self.iRichness)

    def isAtEquilivrium(self, isNr):
        """
        Returns true if island is at aquilibrium. TO MOVE INSIDE ISLAND CLASS
        :param isNr:
        :return:
        """
        equi = True
        richLim = self.timeRichness[isNr][int(len(self.timeRichness[isNr])*0.9)]
        if richLim < self.iRichness[isNr]-(self.islandNr*5) or richLim < self.iRichness[isNr]*0.975:
            equi = False
        return equi

    def sortIslands(self):
        """
        Sorts islands per area. Alters the atribute self.islands so that the first ellemnt in the list
        is the island with the smallest area
        :return: n/A
        """
        a = sorted(self.areas())
        sortedA = [None]*self.islandNr
        for i in range(self.islandNr):
            sortedA[i] = self.islands[self.areas().index(a[i])]
        self.islands = sortedA

    def distMatrix(self):
        """
        Returns a dataframe with the distance matrix
        :return:
        """
        dMatrix = [[]*self.islandNr]*self.islandNr
        for i in range(self.islandNr):
            for j in range(self.islandNr):
              dMatrix.append(self.islands[i].distance(self.islands[j]))

        return dMatrix

