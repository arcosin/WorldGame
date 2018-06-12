
from WorldGenerator import *
from MapImager import printMapGrid, buildMapImage
from UserAgent import UserAgent
from Item import GPSDevice


MACHINE_SPIRIT = [ord(x) for x in "=---<011>---="]

def main():
    testWorldBuild()





def testAgentMovement():
    gen = WorldGenerator()
    world = gen.generateWorld("TestWorld", seed = MACHINE_SPIRIT)
    ua = UserAgent(world, world.coords.getCoord((0, 0)), "User", "The user's agent.")
    ua.backpack.append(GPSDevice())
    while True:   ua.act()


def testWorldBuild():
    gen = WorldGenerator()
    world = gen.generateWorld("TestWorld", seed = MACHINE_SPIRIT)
    buildMapImage(world, "MapImages/Map_%s.png" % world.name)
    world.printWorld()



if __name__ == '__main__':
    main()


#===============================================================================
