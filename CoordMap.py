
from collections import defaultdict


'''
    Builds a coordinate ring in the form of a list.
    In order of w, nw, n, ne, e, se, s, sw.
'''
def coordRing(coord):
    ringCoords = ((coord[0] - 1, coord[1]), (coord[0] - 1, coord[1] + 1),
                  (coord[0], coord[1] + 1), (coord[0] + 1, coord[1] + 1),
                  (coord[0] + 1, coord[1]), (coord[0] + 1, coord[1] - 1),
                  (coord[0], coord[1] - 1), (coord[0] - 1, coord[1] - 1))
    return ringCoords




class CoordMap:
    def __init__(self):
        self.coords = defaultdict(dict)
        self.northestPoint = None
        self.southestPoint = None
        self.eastestPoint = None
        self.westestPoint = None   #Remembers which westest is the bestest.

    def setCoord(self, coord, node):
        if len(coord) == 2:   x, y = coord
        else:   raise ValueError("Coord must have dimmension of 2.")
        if self.northestPoint == None or self.northestPoint[1] < y:
            self.northestPoint = (x, y)
        if self.southestPoint == None or self.southestPoint[1] > y:
            self.southestPoint = (x, y)
        if self.eastestPoint == None or self.eastestPoint[0] < x:
            self.eastestPoint = (x, y)
        if self.westestPoint == None or self.westestPoint[0] > x:
            self.westestPoint = (x, y)
        self.coords[x][y] = node

    def getCoord(self, coord):
        if len(coord) == 2:   x, y = coord
        else:   raise ValueError("Coord must have dimmension of 2.")
        if x in self.coords:
            if y in self.coords[x]:
                return self.coords[x][y]
        return None

    def numCoords(self):
        num = 0
        k = self.coords.keys()
        for x in k:   num = num + len(self.coords[x])
        return num

    def getNeighbors(self, coord):
        if len(coord) != 2:   raise ValueError("Coord must have dimmension of 2.")
        ns = []
        ringCoords = coordRing(coord)
        for i in range(8):
            n = self.getCoord(ringCoords[i])
            ns.append(n)
        return ns

    def getFarthestCoords(self):
        return (self.westestPoint, self.northestPoint, self.eastestPoint, self.southestPoint)

    def buildListGrid(self):
        width = 1 + self.eastestPoint[0] - self.westestPoint[0]
        length = 1 + self.northestPoint[1] - self.southestPoint[1]
        listOrigin = (self.eastestPoint[0], self.northestPoint[1])
        grid = []
        for y in range(length):
            grid.append(list())
            for x in range(width):
                node = self.getCoord((listOrigin[0] - x, listOrigin[1] - y))
                grid[y].append(node)
        return grid



#===============================================================================
