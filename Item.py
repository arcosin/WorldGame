

class Item:
    '''
        Returns info about the item of the form (name, description).
    '''
    def getInfo(self):   raise NotImplementedError()





class Equipment(Item):
    def __init__(self):
        super().__init__()

    def use(self, world, loc):   raise NotImplementedError()





class GPSDevice(Equipment):
    def __init__(self):
        super().__init__()

    def getInfo(self):
        return ("GPS Device", "A small machine that can pinpoint your current coordinate.")

    def use(self, world, loc):
        print("   GPS Coordinate: (%d, %d)" % loc.getWorldCoord())
        print()
