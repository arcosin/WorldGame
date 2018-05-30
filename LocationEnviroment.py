

'''
    An object representing the enviroment of the game location.
    Includes:
        - A biome (from Biome.py)
        - A location name
        - A location description
'''
class LocationEnviroment(object):
    def __init__(self, biome, name = "", descrip = ""):
        self.biome = biome
        self.name = name
        self.descrip = descrip

    def __repr__(self):
        return "{biome:%s, name:%s, descrip:%s}" % (self.biome, self.name, self.descrip)

#===============================================================================
