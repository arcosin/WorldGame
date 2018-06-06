
from WorldGenerator import *
from MapImager import printMapGrid, buildMapImage


MACHINE_SPIRIT = "=---<011>---=hhty"


def main():
    gen = WorldGenerator()
    world = gen.generateWorld("TestWorld", seed = MACHINE_SPIRIT)
    buildMapImage(world, "MapImages/Map_%s.png" % world.name)
    world.printWorld()




if __name__ == '__main__':
    main()


#===============================================================================
