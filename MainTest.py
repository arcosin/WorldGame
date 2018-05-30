
from WorldGenerator import *


MACHINE_SPIRIT = "=---<011>---="


def main():
    gen = WorldGenerator()
    world = gen.generateWorld("Test World", seed = MACHINE_SPIRIT)
    world.printWorld()





if __name__ == '__main__':
    main()


#===============================================================================
