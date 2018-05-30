
import random
from CoordMap import CoordMap, coordRing



class WorldGraph:
    def __init__(self, name):
        self.name=name
        self.idCounter = 0
        self.nodes = []
        self.coords = CoordMap()

    def getNextNodeID(self):
        ret = self.idCounter
        self.idCounter += 1
        return ret

    def addNode(self, node, coord = None):
        node.finished = True
        if coord != None:   self.coords.setCoord(coord, node)
        self.nodes.append(node)


    def printWorld(self):
        for n in self.nodes:   print("%s\n" % n)





class GraphNode(object):
    def __init__(self, id, adjacent = []):
        super().__init__()
        if id < 0:   raise ValueError("Node ID set to negative number.")
        self.id = id
        self.adj = adjacent

    def addAdjacency(self, id):   self.adj.append(id)

    def addAdjacencies(self, ids):   self.adj = self.adj + ids

    def setAdjacency(self, n, id):   self.adj[n] = id

    def getAdjacencies(self):   return list(self.adj)




'''
    A GraphNode representing a world location.
    A location includes:
        - A (non-unique) name
        - An Enviroment object
        - A list of location events
        - A list of items
        - A list of adjacent locations
'''
class Location(GraphNode):
    def __init__(self, id, worldmap, enviroment, adjacent = [], items = [], events = []):
        super().__init__(id, adjacent)
        self.worldmap = worldmap
        self.items = items
        self.events = events
        self.enviroment = enviroment
        self.finished = False

    def getAdjactentLocations(self):   raise NotImplementedError()

    def getWorldCoord(self):   raise NotImplementedError()

    def getItems(self):   return list(self.items)

    def getEvents(self):   return list(self.events)

    def getEnviroment(self):   return self.enviroment

    def setEnviroment(self, enviroment):   self.enviroment = enviroment




'''
    A Location with 8 set directions to travel (0 to 7).
    Adjacencies to PathedLocations may be added additionally.
    Is meant to be infinite and therefore is given a generator.
    If an adjacency is unset, it will be generated on upon request.
'''
class OctagonalLocation(Location):
    def __init__(self, id, worldmap, enviroment, generator, coord, adjacent = [], items = [], events = []):
        super().__init__(id, worldmap, enviroment, adjacent, items, events)
        self.gen = generator
        self.coord = coord

    def addAdjactentPathedLocation(self, id):
        self.addAdjacency(id)

    def getAdjactentLocations(self):
        assert(self.finished)
        octo = self.getOctagonalNeighbors()
        if None in octo:   self.gen.generateOn(self)
        return octo + self.getAdjacencies()

    def getOctagonalNeighbors(self):
        return self.worldmap.coords.getNeighbors(self.coord)

    def getWorldCoord(self):   return self.coord

    def __repr__(self):
        return "OctagonalLocation: {id:%d, env:%s, coord:%s}" % (self.id, str(self.enviroment), str(self.coord))




'''
    A Location with no bound on number of adjacencies.
    Is given an OctogonalLocation as a root.
    Coordinate is reconed using this root location.
'''
class PathedLocation(Location):
    def __init__(self, id, worldmap, enviroment, rootLocationID, adjacent = [], items = [], events = []):
        super().__init__(id, worldmap, enviroment, adjacent, items, events)
        self.root = rootLocationID

    def getAdjactentLocations(self):
        return self.getAdjacencies()

    def addAdjacentLocation(self, id):
        self.addAdjacency(id)

    def getWorldCoord(self):
        return rootLocation.getWorldCoord()

    def __repr__(self):
        return "PathedLocation: {id:%d, env:%s, rootID:%d}" % (self.id, str(self.enviroment), self.rootLocationID)




#===============================================================================
