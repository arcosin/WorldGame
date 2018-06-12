
from Agent import Agent
from WorldGraph import OctagonalLocation
from Toolbox import strToInt
from Item import Equipment

HELP_STR = \
"""
Commands:
"""



class UserAgent(Agent):

    def __init__(self, world, startLoc, name, descrip):
        super().__init__(world, startLoc, name, descrip)
        self.backpack = []


    def act(self):
        cont = True
        while(cont):
            line = input("%s >>   " % self.name).lower()
            toks = line.split(' ')
            if line == "":
                pass
            elif line == "help" or line == "?":
                print(HELP_STR)
                print()
            elif line == "survey":
                self.__survey()
            elif line == "check backpack":
                self.__checkBackpack()
            elif len(toks) == 2 and toks[0] == "move":
                a = strToInt(toks[1])
                if a != None:
                    self.move(a)
                    print()
                    cont = False
                else:
                    print("%s cannot move to %s." % (self.name, toks[1]))
            elif len(toks) >= 2 and toks[0] == "use":
                searchingName = " ".join(toks[1:])
                self.__useEquipment(searchingName)
                print()
            else:
                print("Unknown Command.")
        print("===========================")


    '''
        Move the agent to an adjacent location.
        Arguments:
            a -- index in self.loc.getAdjactentLocations()[0] to move to.
    '''
    def move(self, a):
        adj, _ = self.loc.getAdjactentLocations()
        if a >= 0 and a < len(adj):
            self.loc.agents.remove(self)
            adj[a].agents.append(self)
            self.loc = adj[a]
        else:
            print("%s cannot move to %d." % (self.name, a))


    def __survey(self):
        locEnv = self.loc.getEnviroment()
        _, adjLabels = self.loc.getAdjactentLocations()
        print("Area: %s" % locEnv.name)
        print("Description:\n%s" % locEnv.descrip)
        print()
        for i in range(len(adjLabels)):
            print("   %d -- %s" % (i, adjLabels[i]))
        print()


    def __checkBackpack(self):
        print("Backpack:")
        for i in range(len(self.backpack)):
            print("   %d -- %s" % (i, str(self.backpack[i])))
        print()


    def __useEquipment(self, itemName):
        found = False
        for item in self.backpack:
            if item.getInfo()[0].lower() == itemName:
                if isinstance(item, Equipment):   item.use(self.world, self.loc)
                else:   print("Item is not a piece of equipment.")
                found = True
                break
        if not found:   print("%s does not have this item." % self.name)








#===============================================================================
