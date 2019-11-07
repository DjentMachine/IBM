##
# Testing ground for SAR script
#
# v 0.2
# author: Diogo Barros
##

##
# TODO:
#
# Set randomness on Time = 1 islands. Islands are getting the same Time = 1 richness
#
#
import random

class island:
    """
    Testing for the island class:
        area - area of an island
        richness - species list for a given island
        sourcePop - species list for a source population
        m - migration rate
        e -  extintion rate
        timeRichness - lista de numeros de tamanho x que contem a variação de richness ao longo de x anos.
    """

    def __init__(self, sourcePop, initRichness = 1, isML = False):
        self.isML = isML
        self.area = random.randint(50, 1000)
        self.richness = [0] * len(sourcePop)
        self.sourcePop = sourcePop
        self.m = random.uniform(0.5, 0.6)
        self.e = random.uniform(0.1, 0.2)
        self.iInitiate(initRichness)
        self.timeRichness = [self.gRichness()]


    def iInitiate(self, initRichness):
        """
        Initiates the island with a given species richness sampled from a source
        :param sourcePop: a list (vector) with ints representing the source population richness
        :param initRichness: the chosen initial richness for the island
        :return: n/a
        """
        if self.isML:
            for i in range(initRichness):
                r = random.randint(0,len(self.sourcePop)-1)
                self.richness[r] = 1
        else:
            self.richness = [1] * len(self.sourcePop)



    def iUpdate (self, sourcePop, years=1):
        """
        Update function used to simulate the passage of time. Each update adds a species to Richness based on migration
        (m) and extinguishes another based on the e parameter
        """
        for i in range(years):
            self.sourcePop = sourcePop
            self.migrate()
            self.extinguish()
            self.timeRichness.append(self.gRichness())

    def migrate(self):
        """
        A function that causes migration of 1 random species from one place to another with a given m probability.
        A species only migrates if it exists in Source Population and is not yet on the island
        :param mainLand:
        :param target:
        :return: possibly causes migration of 1 species
        """
        rM = random.uniform(0, 1)
        r1 = random.randint(1, len(self.richness))
        if  self.sourcePop[r1 - 1] == 1 and\
                self.richness[r1 - 1] == 0 and\
                rM < self.m:                        # A species migrates with probability m
                    self.richness[r1 - 1] = 1


    def extinguish(self):
        """
        A function that causes extinction of 1 random species from one place to another with a given m probability
        :param mainLand:
        :param target:
        :return:
        """
        rE = random.uniform(0, 1)
        r2 = random.randint(1, len(self.richness))
        if self.richness[r2 - 1] == 1 and rE < self.e:  # A species goes extinct with prob. e
            self.richness[r2 - 1] = 0


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

    def gRichnessList(self):
        """
        :return: richness list
        """
        return self.richness

    def gM(self):
        """
        :return: m value, for migration, which includes the effect of distance and dispersion
        """
        return self.m

    def gE(self):
        """
        :return: e value, for extinction
        """
        return self.e

    def toString (self):
        """
        To srting method. Shouts a resume of the island atributes
        """
        print("This is a generated island with the following attributes:\n"
              "Area: %d m^2\nCurrent species richness: %d\nInitial Richness: %d species\nMigration rate: %f\nExtinction rate:"
              " %f\nMain land richness: %d\nCurrent species on island:" %
              (self.area, self.gRichness(), self.timeRichness[0],self.m, self.e, len(self.sourcePop)))
        print(self.richness)

class chainedArchipelago:
    """
    Testing for the archipelago class. A normal archipelago has x islands with different m (for distance) and
     e (for extintion) parameters. They all assume the same Main Land.
    """

    def __init__(self, mainLand, islandNumber, initRichness=1, coordRange=[38, -26], aWidth=2):
        self.islandNr = islandNumber
        self.mainLand = mainLand
        self.islands = []
        self.iRichness = []
        self.timeRichness = []
        self.coords = []
        for i in range(islandNumber):
            lat = random.uniform(coordRange[0]-aWidth,coordRange[0]+aWidth)
            lon = random.uniform(coordRange[1]-aWidth,coordRange[1]+aWidth)
            self.coords.append([lat,lon])
            if i == 0:
                self.islands.append(island(mainLand, initRichness))
            else:
                self.islands.append(island(self.islands[i-1].gRichnessList(), initRichness))
            self.iRichness.append(self.islands[i].gRichness())
            self.timeRichness.append(self.islands[i].timeRichness)

    def aUpdate (self, years=1):
        """
        Updates archipelago with each interaction
        """
        for i in range(self.islandNr):
            if i == 0:
                self.islands[i].iUpdate(self.mainLand, years)
            else:
                self.islands[i].iUpdate(self.islands[i-1].gRichnessList(), years)
            self.iRichness[i] = self.islands[i].gRichness()

    def __distMatrix(self, coordMatrix):
        """
        Function to give out distance matrix out of 2 collumns of WGS86 coordinates:
        Latitude first col, longitude 2nd col

        :param coords:
        :return: A distance matrix (list of lists)
        """
        coords = np.deg2rad(coordMatrix)
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


    def richnesses(self):
        """
        Method for creating a list with all richnesses
        """
        r = []
        for i in range(self.islandNr):
            r.append(self.islands[i].area)
        return r

    def toString(self):
        """
        To string method. Shouts a resume of the archipelago's atributes
        """
        print("This is a generated archipelago with the following attributes:\n"
              "Nr of islands: %d\nRichness is the islands:" %
              len(self.islands))
        print(self.iRichness)

class archipelago:
    """
    Testing for the chained archipelago class. A chained archipelago assumes a island is followed
    by a second one whose distance is controled by the parameter "m". Moreover,the first island actas as
    main land to the second one, thus creating a chain effect.
    """

    islands = []
    islandNr = 0
    mainLand = 0



