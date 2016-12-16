from updatewumpus import *

class WumpusHunter:

    def __init__(self):
        self.world = intialize_world()
        self.wumpusFreeMap = set([])
        # self.wum
        self.visitedMap = set([])
        self.pitFreeMap = set([])
        # self.pitMap = set()
        # self.noWallMap = set([  (1, 1), (1, 2), (1, 3), (1, 4),
        #                         (2, 1), (2, 2), (2, 3), (2, 4),
        #                         (3, 1), (3, 2), (3, 3), (3, 4),
        #                         (4, 1), (4, 2), (4, 3), (4, 4)])
        self.wallMap = set([])
        self.safeMap = set([])
        self.smellyMap = set([])

        self.location = None
        self.orrientation = None

        self.hasGold = False
        self.wumpusIsDead = False
        self.hasArrow = True
        self.score = 0
        self.status = ''
        self.won = False
        self.wumpusLocation = False

        self.act("Up")
        self.exit = self.location


    #   Try to locate the wumpus, using the smell info
    def locateWumpus(self):
        adjSmellyRooms = []
        for smellyRoom in self.smellyMap:
            adjSmellyRooms.append(set(self.getAdjacentRooms(smellyRoom)))

        possibleWumpusRooms = reduce(lambda a, b: a & b, adjSmellyRooms)

        # possibleWumpusRooms = set([])
        # if len(adjSmellyRooms) > 1:
        #
        #     possibleWumpusRooms = adjSmellyRooms[0] & adjSmellyRooms[1]
        #     for i in xrange(2, len(adjSmellyRooms)):
        #         possibleWumpusRooms &= possibleWumpusRooms

        possibleWumpusRooms -= self.safeMap
        if len(possibleWumpusRooms) == 1:
            self.wumpusLocation = list(possibleWumpusRooms)[0]
            return self.wumpusLocation
        else:
            return False


    #   step into an adjacent room
    def stepTo(self, direction):
        self.act(self.getDirection(self.location, direction))
        self.act('Step')


    #   Try to take a safe route to some safe place
    def safeGoto(self, target):
        def findSafeRoute(curr, target, safeRoom):
            if curr == target: return [target]

            # result = []
            for adjRoom in self.getAdjacentRooms(curr):
                if adjRoom in safeRoom:
                    res = findSafeRoute(adjRoom, target, safeRoom-set([adjRoom]))
                    if res: return [curr] + res
            return False

        safeRoute = findSafeRoute(self.location, target, self.safeMap)

        try:
            for i in xrange(1, len(safeRoute)):
                self.stepTo(safeRoute[i])
        except:
            self.safeGoto(target)


    #   Take an action
    def act(self, move):
        # print '?? %s' % str(move)
        self.updateStatus(take_action(self.world, move))


    #   update current status, usually happen after an action
    def updateStatus(self, actionResult):
        # ['nasty', 'calm', 'bare', 'no_bump', 'quiet', u'Cell 12', 'Down', 'living', 0]
        self.wumpusIsDead = False if actionResult[4] == 'quiet' else True
        self.location = tuple([int(c) for c in actionResult[5][-2:]])

        self.visitedMap.add(self.location)
        self.orrientation = actionResult[6]
        self.status = actionResult[7]
        self.score = actionResult[8]

        self.updateWumpusMap(True if actionResult[0] == 'nasty' else False)
        self.updatePitMap(True if actionResult[1] == 'breeze' else False)
        self.tryToPickGold(True if actionResult[2] == 'glitter' else False)
        self.updateWallMap(True if actionResult[3] == 'bump' else False)

        self.updateSafeRoom()
        # print self.wallMap


    #   Try to kill the wumpus, first move near to wumpus, then shoot
    def killWumpus(self):
        nearWumpusLocs = set(self.getAdjacentRooms(self.wumpusLocation)) & self.safeMap
        self.safeGoto(list(nearWumpusLocs)[0])
        self.act(self.getDirection(self.location, self.wumpusLocation))
        self.act('Shoot')
        self.hasArrow = False


    #   take an action, try to kill the wumpus and pick up the gold
    #   but don't take risk, if it's not sure, don't risk your life
    def mission(self):
        unVisitedRoom = self.safeMap - self.visitedMap

        for room in unVisitedRoom:
            self.safeGoto(room)

        if self.hasArrow and self.locateWumpus():
            self.killWumpus()

        if self.checkIfWon():
            print "Yes!"
        elif self.safeMap - self.visitedMap:
            self.mission()
        else:
            self.safeGoto(self.exit)
            self.act('Exit')
            print 'Don\'t get caught'
            # print self.score

            return None


    #   find the direction between target and current location
    def getDirection(self, curr, target):
        lr = target[0] - curr[0]
        ud = target[1] - curr[1]
        if lr:
            return 'Right' if lr > 0 else 'Left'
        if ud:
            return 'Up' if ud > 0 else 'Down'


    #   Check if we already won, if won, just take a safe road to exit.
    def checkIfWon(self):
        if self.score == 1100:
            self.safeGoto(self.exit)
            self.act('Exit')
            return True


    #   update which room is safe
    def updateSafeRoom(self):
        self.safeMap.add(self.location)

        for room in self.getAdjacentRooms(self.location):
            if room in self.wumpusFreeMap and room in self.pitFreeMap:
                self.safeMap.add(room)
        # self.safeMap &= self.noWallMap
        self.safeMap -= self.wallMap


    #   Update which room has no wumpus, which place has smell
    def updateWumpusMap(self, hasSmell):
        if hasSmell:
            self.smellyMap.add(self.location)
        #     print ''
        else:
            for room in self.getAdjacentRooms(self.location):
                self.wumpusFreeMap.add(room)


    #   Update which room has no pit, don't care about where the pit actually is
    def updatePitMap(self, hasBreeze):
        if not hasBreeze:
        # else:
            for room in self.getAdjacentRooms(self.location):
                self.pitFreeMap.add(room)


    #   Update which place has wall
    def updateWallMap(self, hasBump):
        if hasBump:
            self.wallMap.add(self.getForwardRoom())
            self.safeMap -= self.wallMap


    #   Check if there are gold, if there are gold, pick it up!
    def tryToPickGold(self, hasGold):
        if hasGold:
            self.act('PickUp')
            # Do something


    #   Get all the room that near a location
    def getAdjacentRooms(self, location):
        i, j = location
        return [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]


    #   find out which room is in front of us
    def getForwardRoom(self):
        i, j = self.location
        return {'Left':(i-1, j), 'Right':(i+1, j), 'Down':(i, j-1), 'Up':(i, j+1)}[self.orrientation]


if __name__ == '__main__':
    hunter = WumpusHunter()
    hunter.mission()
