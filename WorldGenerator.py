
import random
from WorldGraph import *
from Item import *
from Event import *
from LocationEnviroment import LocationEnviroment
from Biomes import BIOME_DEFINITIONS, BIOMES, BIOME_TRANSFORMS
from CoordMap import CoordMap, coordRing




class WorldGenerator:

    '''
        Generates a populated WorldGraph.
        Arguments:
            name -- name string of the world.
            seed -- RNG seed used to generate the world. string or int.
    '''
    def generateWorld(self, name, seed = None):
        random.seed(seed)
        world = WorldGraph(name)
        self.worldName = name
        start = self.generateStartingPoint(world)
        w, nw, n, ne, e, se, s, sw = self.generateDefaultStartingRing(world)
        self.generateOn(world, nw)
        self.generateOn(world, ne)
        self.generateOn(world, se)
        self.generateOn(world, sw)
        return world


    '''
        Used to incrementally build the WorldGraph.
        Arguments:
            world -- worldmap in use.
            node -- the OctagonalLocation to be built on.
    '''
    def generateOn(self, world, node):
        neighbors = world.coords.getNeighbors(node.coord)
        ringCoords = coordRing(node.coord)
        for i in range(8):
            if neighbors[i] == None:   #check that space is vacent.
                chunk = self.generateRandomChunk(world, ringCoords[i], node)   #Generate a new chunk.
                for loc in chunk:   world.addNode(loc, loc.coord)   #Add the generated chunk to the world.
                neighbors = world.coords.getNeighbors(node.coord)   #Recalculate neighbors.


    '''
        Generates the "The Village on the Plains".
        Arguments:
            world -- worldmap in use.
    '''
    def generateStartingPoint(self, world):
        id = world.getNextNodeID()
        bio = "start_village"
        envName = BIOME_DEFINITIONS[bio][0]
        envDesc = BIOME_DEFINITIONS[bio][1]
        env = LocationEnviroment(bio, envName, envDesc)
        adj = []
        villageItems = []
        villageEvents = []
        start = OctagonalLocation(id, world, env, self, (0, 0), adj, villageItems, villageEvents)
        world.addNode(start, (0, 0))
        return start


    '''
        Generates the ring of OctagonalLocations around the starting village.
        Arguments:
            world -- worldmap in use.
    '''
    def generateDefaultStartingRing(self, world):
        ring = [None] * 8
        ringCoords = coordRing((0, 0))
        for i in range(8):
            id = world.getNextNodeID()
            bio = "plains"
            envName = BIOME_DEFINITIONS[bio][0]
            envDesc = BIOME_DEFINITIONS[bio][1]
            env = LocationEnviroment(bio, envName, envDesc)
            items = []
            events = []
            adj = []
            ring[i] = OctagonalLocation(id, world, env, self, ringCoords[i], adj, items, events)
            world.addNode(ring[i], ringCoords[i])
        return ring


    '''
        Generate a random chunk of locations.
        Arguments:
            world -- worldmap in use.
            rootCoord -- empty coord from which chunk is built.
            rootNode -- node which chunk is based on. None by default.
            maxExp -- maximum number of locations grown from the start coord.
        Checks if it should be a special chunk.
        If not special, decides the generated biome.
        Next, generates the locations.
        Returns a list of locations to be added.
    '''
    def generateRandomChunk(self, world, rootCoord, rootNode = None):
        neighbors = world.coords.getNeighbors(rootCoord)
        #TODO: add special chunks.
        rootBiome = rootNode.getEnviroment().biome
        biome = random.choice(BIOME_TRANSFORMS[rootBiome])
        coordSet = self.recursiveRandomGridBuild(world, rootCoord)   #Generate structure of the chunk.
        chunk = []
        for coord in coordSet:   #Add OctagonalLocation on each coord in chunk.
            id = world.getNextNodeID()
            envName = BIOME_DEFINITIONS[biome][0]
            envDesc = BIOME_DEFINITIONS[biome][1]
            items = []
            events = []
            adj = []
            env = LocationEnviroment(biome, envName, envDesc)
            chunk.append(OctagonalLocation(id, world, env, self, coord, adj, items, events))
        return chunk


    '''
        Determines structure of a chunk based on probabilities.
        Arguments:
            world -- worldmap in use.
            rootCoord -- coord from which chunk structure is built (recursively).
            probStop -- probability that growth will stop before next node.
            probInc -- amount to increment probStop each generation.
        Returns a set of coordinates (x, y) to build on.
    '''
    def recursiveRandomGridBuild(self, world, rootCoord, probStop = 0.4, probInc = 0.1):
        neighbors = world.coords.getNeighbors(rootCoord)
        ringCoords = coordRing(rootCoord)
        addedCoords = set()
        recCoords = {rootCoord}
        for i in range(len(neighbors)):
            if neighbors[i] == None:
                stop = random.random() < probStop
                if not stop:   addedCoords.add(ringCoords[i])
        for coord in addedCoords:
            rec = self.recursiveRandomGridBuild(world, coord, probStop = probStop + probInc, probInc = probInc)
            recCoords = recCoords.union(rec)
        return recCoords














































#===============================================================================
