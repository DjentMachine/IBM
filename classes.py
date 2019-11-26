##
# Testing ground for SAR script
#
# v 0.2
# author: Diogo Barros
##

##
# TODO: Take care of variable AMax. It's not set to 1000, as its the max possible value
##

import random
import numpy as np
from math import sqrt
import math

class island:
    """
    Constructor for the island class:
        popSize -
        initRichness -
        isML -
        area - area of an island
        richness - species list for a given island
    """

    def __init__(self, sppCapacity, isML=False, coordRange=[38, -26], aWidth=2, initRichness = 1):
        self.isML = isML
        self.area = random.randint(50, 1000)
        self.coords = coordRange
            #[random.uniform(coordRange[0] - aWidth, coordRange[0] + aWidth),
             #          random.uniform(coordRange[1] - aWidth, coordRange[1] + aWidth)]
        if isML: self.richness = [1] * sppCapacity
        else: self.richness = [0] * sppCapacity
        self.iInitiate(initRichness)
        self.timeRichness = []

    def iInitiate(self, initRichness):
        """
        Initiates the island with a given species richness sampled from a source
        :param sourcePop: a list (vector) with ints representing the source population richness
        :param initRichness: the chosen initial richness for the island
        :return: n/a
        """
        if not self.isML:
            for i in range(initRichness):
                r = random.randint(0,len(self.richness)-1)
                self.richness[r] = 1
        self.timeRichness = self.gRichness()

    def update(self):
        """
        Updates island with migration and extinction. WIP
        :return:
        """
        self.timeRichness.append(self.gRichness())

    def migrate(self, sourceIsland):
        """
        A function that causes migration of 1 random species from one place to another with a given m probability.
        A species only migrates if it exists in Source Population and is not yet on the island
        :param mainLand:
        :param target:
        :return: possibly causes migration of 1 species
        """
        rM = random.uniform(0, 1)
        #mCoeff = random.uniform(0.8, 1)*(math.e**(-self.distance(sourceIsland)/100000)) #The Bigger, the more likely to migrate
        epsilon = math.e**(-self.distance(sourceIsland)/100000) #The Bigger, the more likely to migrate
        iRate = 1-epsilon*(self.gRichness()/len(self.richness))**(self.area/1000) #1000 = maxArea
        rPosition = random.randint(0, len(self.richness)-1)
        if self.richness[rPosition] == 0 and \
                rM < iRate:  # A species migrates with probability m
            self.richness[rPosition] = 1

    def extinguish(self):
        """
        A function that causes extinction of 1 random species from one place to another with a given m probability
        :param mainLand:
        :param target:
        :return:
        """
        rE = random.uniform(0, 1)
        #eCoeff = random.uniform(0, 0.1)
        gamma = random.uniform(0, 0.1)
        eRate = gamma*(self.gRichness()/len(self.richness))**(1/self.area)
        rPosition = random.randint(0, len(self.richness)-1)
        if self.richness[rPosition] == 1 and \
            rE < eRate:  # A species goes extinct  with probability e
            self.richness[rPosition] = 0

    def distance(self, sourceIsland):
        """
        Calculates distance between 2 islands
        :return:
        """
        dlat = np.deg2rad(self.coords[0] - sourceIsland.coords[0])
        dlon = np.deg2rad(self.coords[1] - sourceIsland.coords[1])
        hav = (np.sin(dlat / 2)) ** 2 + np.cos(self.coords[1]) * np.cos(sourceIsland.coords[1])\
              * (np.sin(dlon / 2)) ** 2
        return 2 * np.arctan2(sqrt(hav), sqrt(1 - hav)) * 6378100  # c * R , where R=6378100 is the radius of the Earth

    def gArea(self):
        """
        :return: area value for each island
        """
        return self.area

    def gRichness(self):
        """
        :return: total species richness for the island
        """

        return sum(1 for x in self.richness if x == 1)

    def toString (self):
        """
        To string method. Shouts a resume of the island atributes
        """
        print("This is a generated island with the following attributes:\n"
              "Area: %d m^2\nCurrent number of species: %d\nCurrent species on island: " %
              (self.area, self.gRichness()))
        print(self.richness)

class chainedArchipelago:
    """
    Testing for the archipelago class. A normal archipelago has x islands with different m (for distance) and
     e (for extintion) parameters. They all assume the same Main Land.
    """

    def __init__(self, sppCapacity, islandNr, initRichness=1, coordRange=[38, -26], aWidth=2):
        self.islandNr = islandNr
        self.mainLand = island(sppCapacity, isML=True)
        self.islands = []
        self.iRichness = []
        self.timeRichness = [[] for i in range(islandNr)]
        self.iCoords = []
        for i in range(islandNr):
            self.islands.append(island(sppCapacity, False, coordRange, aWidth, initRichness))
            self.iRichness.append(self.islands[i].gRichness())
            self.timeRichness[i].append(self.iRichness[i])
            self.iCoords.append(self.islands[i].coords)


    def aUpdate (self, years=1):
        """
        Updates archipelago with each interaction
        """
        for i in range(years):
            for j in range(self.islandNr):
                self.aMigrate()
                self.aExtinguish()
                self.iRichness[j] = self.islands[j].gRichness()
                self.timeRichness[j].append(self.islands[j].gRichness())


    def aMigrate(self):
        """
        Causes migration from 1 neighbouring island to a target island with a probability m
        :param island:
        :return:
        """
        for i in range(self.islandNr):
            for j in range(self.islandNr):
                self.islands[i].migrate(self.islands[j])

    def aExtinguish(self):
        """
        Extinguishes one species form an island in an archipelago with a probability e
        :param island:
        :return:
        """
        for i in range(self.islandNr):
            self.islands[i].extinguish()

    def gTimeRichness(self, islandNr, min, max):
        """
        Returns the richness from a given island from a set interval of time
        :param island:
        :return: a vector with the time richness
        """
        return self.timeRichness[islandNr][min:max]



    def distMatrix(self, coordsMatrix):
        """
        Function to give out distance matrix out of 2 collumns of WGS86 coordinates:
        Latitude first col, longitude 2nd col

        :param coords:
        :return: A distance matrix (list of lists)
        """
        coords = np.deg2rad(coordsMatrix)
        dist = [[0 for col in range(len(coords))] for row in range(len(coords))]
        for i in range(len(dist)):
            for j in range(len(dist[0])):
                dlat = coords[j][0] - coords[i][0]
                dlon = coords[j][1] - coords[i][1]
                hav = (np.sin(dlat / 2)) ** 2 + np.cos(coords[i][1]) * np.cos(coords[j][1]) * (np.sin(dlon / 2)) ** 2
                c = 2 * np.arctan2(sqrt(hav), sqrt(1 - hav))
                r = 6378100  # where R is the radius of the Earth
                dist[i][j] = r * c
        return dist

    def spatialAutocorr(self, coords):
        """
        Integrates spatial autocorrelation. Used in the migration function
        :return:
        """


    def areas (self):
        """
        Method for creating a list with all areas
        """
        a = []
        for i in range(islandNr):
            a.append(islands[i].area)
        return a


    def toString(self):
        """
        To string method. Shouts a resume of the archipelago's atributes
        """
        print("This is a generated archipelago with the following attributes:\n"
              "Nr of islands: %d\nRichness is the islands:" %
              len(self.islands))
        print(self.iRichness)


#Er = extinction rate
#Ir  immigration rate

#Ir=1-epsilon(S/ST)^+alpha  ; 0<=alpha<1; E<1
#Er=gamma(b/ST)^beta ; 1<= beta, gamma<1

#Ir=Er -> Equilibrium:Seq

#Aplha=A/Amax
#Beta=1/a ou Beta = Amax/A (need to define Amax)


