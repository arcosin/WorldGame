
import random
from CoordMap import CoordMap, coordRing



class WorldGraph:
    def __init__(self, name, rng = None):
        self.name=name
        self.idCounter = 0
        self.chunkCounter = 1
        self.rng = rng
        self.nodes = []
        self.coords = CoordMap()

    def getNextNodeID(self):
        ret = self.idCounter
        self.idCounter += 1
        return ret

    def getNextChunkID(self):
        ret = self.chunkCounter
        self.chunkCounter += 1
        return ret

    def addNode(self, node, coord = None):
        node.finished = True
        if coord != None:   self.coords.setCoord(coord, node)
        self.nodes.append(node)

    def printWorld(self):
        for n in self.nodes:   print("%s\n" % str(n))




'''
    A class representing the simple functionality of a graph node.
    Includes a list of adjacency pointers and a positive number id.
'''
class GraphNode(object):
    def __init__(self, id, adjacent = []):
        super().__init__()
        if id < 0:   raise ValueError("Node ID set to negative number.")
        self.id = id
        self.adj = adjacent

    def addAdjacency(self, node):   self.adj.append(node)

    def addAdjacencies(self, nodes):   self.adj = self.adj + nodes

    def setAdjacency(self, n, node):   self.adj[n] = node

    def getAdjacencies(self):   return list(self.adj)




'''
    A GraphNode representing a world location.
    A location includes:
        - A (non-unique) name
        - An Enviroment object
        - A list of location events
        - A list of items
        - A list of agents currently in the room.
        - A list of labels for each adj.
        - A list of adjacent locations
'''
class Location(GraphNode):
    def __init__(self, id, worldmap, enviroment, adjacent = [], adjLabels = []):
        super().__init__(id, adjacent)
        assert(len(adjacent) == len(adjLabels))
        self.worldmap = worldmap
        self.items = []
        self.events = []
        self.agents = []
        self.adjLabels = adjLabels
        self.chunkID = -1     #Optional field to store a locations "chunk" or grouping. -1 = unset.
        self.enviroment = enviroment
        self.finished = False

    '''
        Returns all adjacent locations.
        Returned in the form (list_of_adj_locs, list_of_labels).
    '''
    def getAdjactentLocations(self):   raise NotImplementedError()

    def getWorldCoord(self):   raise NotImplementedError()

    def addAdjactentLocation(self, loc, label):
        self.addAdjacency(loc)
        self.adjLabels.append(label)

    def getItems(self):   return list(self.items)

    def getEvents(self):   return list(self.events)

    def setItems(self, items):   self.items = items

    def setEvents(self, events):   self.events = events

    def setChunkID(self, id):   self.chunkID = id

    def getChunkID(self):   return self.chunkID

    def getEnviroment(self):   return self.enviroment

    def setEnviroment(self, enviroment):   self.enviroment = enviroment




'''
    A Location with 8 set directions to travel (0 to 7).
    These 8 directions do not need to be explicitly added.
    Adjacencies to PathedLocations may be added additionally.
    Is meant to be an infinite grid and therefore is given a generator.
    If an adjacency is unset, it will be generated on upon request.
'''
class OctagonalLocation(Location):
    def __init__(self, id, worldmap, enviroment, generator, coord, adjacent = []):
        super().__init__(id, worldmap, enviroment, adjacent)
        self.gen = generator
        self.coord = coord

    '''
        Returns all adjacent locations (First 8 are directional locs).
        Will generate new chunks if a directional loc is uninitialized.
    '''
    def getAdjactentLocations(self):
        assert(self.finished)
        octo = self.getOctagonalNeighbors()
        octoLabels = ['W', 'NW', 'N', 'NE', 'E', 'SE', 'S', 'SW']
        while None in octo:
            self.gen.generateOn(self.worldmap, self)
            octo = self.getOctagonalNeighbors()
        return (octo + self.getAdjacencies(), octoLabels + list(self.adjLabels))

    def getOctagonalNeighbors(self):
        return self.worldmap.coords.getNeighbors(self.coord)

    def getWorldCoord(self):   return self.coord

    def __repr__(self):
        return "OctagonalLocation: {id:%d, coord:%s, chunkID:%d, env:%s}" % (self.id, str(self.coord), self.chunkID, str(self.enviroment))




'''
    A Location with no bound on number of adjacencies.
    Is given an OctogonalLocation as a root.
    Coordinate is reconed using this root location.
'''
class PathedLocation(Location):
    def __init__(self, id, worldmap, enviroment, rootLocationID, adjacent = []):
        super().__init__(id, worldmap, enviroment, adjacent)
        self.root = rootLocationID

    def getAdjactentLocations(self):
        return (self.getAdjacencies(), list(self.adjLabels))

    def getWorldCoord(self):
        return rootLocation.getWorldCoord()

    def __repr__(self):
        return "PathedLocation: {id:%d, rootID:%d, chunkID:%d, env:%s}" % (self.id, self.rootLocationID, self.chunkID, str(self.enviroment))





#===============================================================================
