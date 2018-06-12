

class Agent:
    numAgents = 0

    def __init__(self, world, startLoc, name, descrip):
        self.id = Agent.numAgents
        self.world = world
        self.loc = startLoc
        self.name = name
        self.descrip = descrip
        Agent.numAgents += 1
        startLoc.agents.append(self)

    def act(self):   raise NotImplementedError()

    def getInfo(self):
        return (self.id, self.name, self.descrip)
