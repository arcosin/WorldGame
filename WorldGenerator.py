
from WorldGraph import *
from Item import *
from Event import *
from LocationEnviroment import LocationEnviroment
from Biomes import BIOME_DEFINITIONS, BIOME_TRANSFORMS, buildBiomeFreqList
from CoordMap import CoordMap, coordRing
from MapImager import buildMapImage
from numpy.random import RandomState




class WorldGenerator:

    temp_count = 1

    '''
        Generates a populated WorldGraph.
        Arguments:
            name -- name string of the world.
            seed -- RNG seed used to generate the world. string or int.
    '''
    def generateWorld(self, name, seed = None):
        world = WorldGraph(name, rng = RandomState(seed=seed))
        self.worldName = name
        start = self.generateStartingPoint(world)
        w, nw, n, ne, e, se, s, sw = self.generateDefaultStartingRing(world)
        buildMapImage(world, "MapImages/Map_%s_t0.png" % world.name)
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
                self.generateRandomChunk(world, ringCoords[i], node)   #Generate and add a new chunk.
                neighbors = world.coords.getNeighbors(node.coord)   #Recalculate neighbors.
        buildMapImage(world, "MapImages/Map_%s_t%d.png" % (world.name, WorldGenerator.temp_count))
        WorldGenerator.temp_count = WorldGenerator.temp_count + 1


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
        start = OctagonalLocation(id, world, env, self, (0, 0), adj)
        start.setChunkID(0)
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
            adj = []
            ring[i] = OctagonalLocation(id, world, env, self, ringCoords[i], adj)
            ring[i].setChunkID(0)
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
        Next, generates the locations and adds them to the world.
        Returns a list of locations to be added.
    '''
    def generateRandomChunk(self, world, rootCoord, rootNode = None):
        neighbors = world.coords.getNeighbors(rootCoord)
        chunkID = world.getNextChunkID()
        #TODO: add special chunks.
        rootBiome = rootNode.getEnviroment().biome
        biomeTrans = BIOME_TRANSFORMS[rootBiome]
        biome = world.rng.choice(biomeTrans, p = buildBiomeFreqList(biomeTrans))
        coordSet = self.recursiveRandomGridBuild(world, rootCoord)   #Generate structure of the chunk.
        for coord in coordSet:   #Add OctagonalLocation on each coord in chunk.
            id = world.getNextNodeID()
            envName = BIOME_DEFINITIONS[biome][0]
            envDesc = BIOME_DEFINITIONS[biome][1]
            adj = []
            env = LocationEnviroment(biome, envName, envDesc)
            loc = OctagonalLocation(id, world, env, self, coord, adj)
            loc.setChunkID(chunkID)
            world.addNode(loc, coord)


    '''
        Determines structure of a chunk based on probabilities.
        Arguments:
            world -- worldmap in use.
            rootCoord -- coord from which chunk structure is built (recursively).
            probStop -- probability that growth will stop before next node.
            probInc -- amount to increment probStop each generation.
        Returns a set of coordinates (x, y) to build on.
    '''
    def recursiveRandomGridBuild(self, world, rootCoord, probStop = 0.4, probInc = 0.15):
        neighbors = world.coords.getNeighbors(rootCoord)
        ringCoords = coordRing(rootCoord)
        addedCoords = set()
        recCoords = {rootCoord}
        for i in range(len(neighbors)):
            if neighbors[i] == None:
                stop = world.rng.random_sample() < probStop
                if not stop:   addedCoords.add(ringCoords[i])
        for coord in addedCoords:
            rec = self.recursiveRandomGridBuild(world, coord, probStop = probStop + probInc, probInc = probInc)
            recCoords = recCoords.union(rec)
        return recCoords














































#===============================================================================
