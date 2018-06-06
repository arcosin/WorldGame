
import random
from CoordMap import CoordMap, coordRing



class WorldGraph:
    def __init__(self, name):
        self.name=name
        self.idCounter = 0
        self.chunkCounter = 1
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
    def __init__(self, id, worldmap, enviroment, adjacent = []):
        super().__init__(id, adjacent)
        self.worldmap = worldmap
        self.items = []
        self.events = []
        self.chunkID = -1     #Optional field to store a locations "chunk" or grouping. -1 = unset.
        self.enviroment = enviroment
        self.finished = False

    def getAdjactentLocations(self):   raise NotImplementedError()

    def getWorldCoord(self):   raise NotImplementedError()

    def getItems(self):   return list(self.items)

    def getEvents(self):   return list(self.events)

    def setItems(self, items):   self.items = items

    def setEvents(self, events):   self.events = events

    def addItem(self, item):   self.items.append(item)

    def addEvent(self, event):   self.events.append(event)

    def delItem(self, i):   del self.items[i]

    def delEvent(self, i):   del self.events[i]

    def setChunkID(self, id):   self.chunkID = id

    def getChunkID(self):   return self.chunkID

    def getEnviroment(self):   return self.enviroment

    def setEnviroment(self, enviroment):   self.enviroment = enviroment




'''
    A Location with 8 set directions to travel (0 to 7).
    Adjacencies to PathedLocations may be added additionally.
    Is meant to be infinite and therefore is given a generator.
    If an adjacency is unset, it will be generated on upon request.
'''
class OctagonalLocation(Location):
    def __init__(self, id, worldmap, enviroment, generator, coord, adjacent = []):
        super().__init__(id, worldmap, enviroment, adjacent)
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
        return self.getAdjacencies()

    def addAdjacentLocation(self, id):
        self.addAdjacency(id)

    def getWorldCoord(self):
        return rootLocation.getWorldCoord()

    def __repr__(self):
        return "PathedLocation: {id:%d, rootID:%d, chunkID:%d, env:%s}" % (self.id, self.rootLocationID, self.chunkID, str(self.enviroment))




#===============================================================================
