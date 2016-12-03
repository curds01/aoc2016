# The Document indicates that you should start at the given coordinates (where you just
# landed) and face North. Then, follow the provided sequence: either turn left (L) or
# right (R) 90 degrees, then walk forward the given number of blocks, ending at a new
# intersection.
#
# There's no time to follow such ridiculous instructions on foot, though, so you take a
# moment and work out the destination. Given that you can only walk on the street grid of
# the city, how far is the shortest path to the destination?

import os
os.chdir(os.path.split(__file__)[0])

class Address:
    def __init__( self, x, y ):
        self.x = x
        self.y = y

    def __getitem__( self, i ):
        if ( i == 0 ):
            return self.x
        elif ( i == 1 ):
            return self.y

    def __add__( self, a ):
        return Address( self.x + a.x, self.y + a.y )

    def tuple( self ):
        return (self.x, self.y)

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

DELTA = {NORTH:Address( 0, 1 ),
         EAST:Address( 1, 0 ),
         SOUTH:Address( 0, -1 ),
         WEST:Address( -1, 0 )
         }
         
class Step:
    LEFT = -1
    RIGHT = 1
    '''Definition of operation'''
    def __init__( self, turn, dist ):
        self.turn = turn
        self.dist = dist

class Agent:
    '''The agent that is moving through the street'''
    
    def __init__( self ):
        self.pos = Address(0, 0)
        self.dir = NORTH
        self.history = set()
        self.actual_locale = None
        self.updateHistory()

    def updateHistory( self ):
        p = self.pos.tuple()
##        print p
        if ( self.actual_locale is None and p in self.history ):
            self.actual_locale = p
        self.history.add( p )

    def takeStep( self, step ):
        self.dir = (self.dir + step.turn ) % 4
        delta = DELTA[ self.dir ]
        for i in xrange( step.dist ):
            self.pos = self.pos + delta
            self.updateHistory()

    def distance( self ):
        '''Returns the distance from the origin to current position'''
        return abs(self.pos[0]) + abs(self.pos[1])

    def actual_distance( self ):
        '''Returns the distance from the origin to the *actual locale*'''
        return abs(self.actual_locale[0]) + abs(self.actual_locale[1])

    def __str__( self ):
        s = "Agent at (%d, %d) at distance %d" % ( self.pos[0], self.pos[1], self.distance() )
        if ( self.actual_locale is not None ):
            s += ", actual distance: %d" % self.actual_distance()
        return s

def getStepList( instructions ):
    '''Given the instructions encoded as a comma-separated string where each step is
    {R|L}D, returns a list of Step instances.
    '''
    dir_map = {'R':Step.RIGHT, 'L':Step.LEFT}
    tokens = map( lambda x: x.strip(), instructions.split(',') )
    def tokToStep( tok ):
        return Step(dir_map[tok[0]], int(tok[1:]))
    return map( lambda x: tokToStep(x), tokens)

def walk( instructions ):
    print instructions
    steps = getStepList( instructions )
    a = Agent()
    for s in steps:
        a.takeStep(s)
    return a
    
def test():
    a = walk( 'R2, L3' )
    print a

    a = walk( 'R2, R2, R2' )
    print a

    a = walk( 'R5, L5, R5, R3' )
    print a

    a = walk( 'R8, R4, R4, R8' )
    print a

def problem():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        inst = ''.join(lines)
        a = walk( inst )
        print a  

if __name__ == '__main__':
##    test()
    problem()
    