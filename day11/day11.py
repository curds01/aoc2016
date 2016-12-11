# My solution to the advent of code 2016 day 11 puzzle

import os
os.chdir(os.path.split(__file__)[0])
import numpy as np
import re
import sys

THULIUM = 'TH'
PLUTONIUM = 'PL'
STRONTIUM = 'ST'
PROMETHIUM = 'PR'
RUTHENIUM = 'RU'

class Floor:
    def __init__( self, floor_num, items ):
        self.floor_num = floor_num
        self.gen = []
        self.chip = []
        self.append( items )
        
    def __str__( self ):
        s = 'F%d:' % ( self.floor_num )
        s += ''.join( map( lambda x: '{0:>5}'.format( x ), self.gen ) )
        s += ''.join( map( lambda x: '{0:>5}'.format( x ), self.chip) )
        return s

    def __len__( self ):
        return len( self.gen ) + len( self.chip )

    def __getitem__( self, i ):
        if ( i < len( self.gen ) ):
            return self.gen[ i ]
        else:
            return self.chip[ i - len( self.gen ) ]

    def items( self ):
        return self.gen + self.chip

    def __repr__( self ):
        return str(self )

    def pop( self, ids ):
        '''Creates a version of this floor with the ith item removed.

        @returns a tuple (item, floor).'''
        items = self.gen + self.chip
        ids.sort()
        results = []
        for id in ids[::-1]:
            results.append( items.pop( id ) )
##        item = items.pop( i )
        floor = Floor( self.floor_num, items )
        return results, floor

    def test( self, items ):
        '''Tests to see if the addition of these items would lead to a valid floor state.
        '''
        f = Floor( -1, self.gen + self.chip + items )
        return f.isValid()

    def isEmpty( self ):
        return len( self.gen ) + len( self.chip ) == 0

    def isValid( self ):
        if ( self.isEmpty() ):
            return True
        else:
            if ( len( self.gen ) == 0 ): return True
            elif ( len( self.chip ) == 0 ): return True
            else:
                for m in self.chip:
                    if m not in self.gen: return False
                return True

    def append( self, items ):
        self.gen.extend( filter( lambda x: x.__class__ is Generator, items ) )
        self.chip.extend( filter( lambda x: x.__class__ is Microchip, items ) )

    def remove( self, items ):
        for item in items:
            if ( item.__class__ is Microchip ):
                self.chip.pop( self.chip.index( item ) )
            elif ( item.__class__ is Generator ):
                self.gen.pop( self.gen.index( item ) )
        


class Item:
    ID = 0
    def __init__( self ):
        self.id = Item.ID
        Item.ID += 1

    def hash( self, floor ):
        '''Assume floor in the range [0-3].
        Pushes the two lowest bits left id * 2 bits'''
        return (floor & 3) << (self.id * 2 )

    def __repr__( self ):
        return str( self )

class Generator(Item):
    def __init__( self, type ):
        Item.__init__( self )
        self.type = type

    def __str__( self ):
        return 'G_%s' % self.type

    def __eq__( self, m ):
        return self.type == m.type
        
class Microchip(Item):
    def __init__( self, type ):
        Item.__init__( self )
        self.type = type
        
    def __str__( self ):
        return 'M_%s' % self.type

    def __eq__( self, g ):
        return self.type == g.type

FLOORS = [ Floor( 1, [ Generator(THULIUM), Microchip(THULIUM), Generator(PLUTONIUM), Generator(STRONTIUM) ] ), # floor 1
           Floor( 2, [ Microchip(PLUTONIUM), Microchip(STRONTIUM) ]), # floor 2
           Floor( 3, [ Generator(PROMETHIUM), Microchip(PROMETHIUM), Generator(RUTHENIUM), Microchip(RUTHENIUM) ] ), # floor 3
           Floor( 4, [] ) # floor 4
           ]

##FLOORS = [ Floor( 1, [ Microchip('H'), Microchip('L') ] ),
##           Floor( 2, [ Generator('H'), ] ),
##           Floor( 3, [ Generator('L') ] ),
##           Floor( 4, [ ] )
##           ]

##FLOORS = [ Floor( 1, [ Microchip('L'),  ] ),
##           Floor( 2, [  ] ),
##           Floor( 3, [ Microchip('H'), Generator('L'), Generator('H') ] ),
##           Floor( 4, [ ] )
##           ]

HISTORY = set()

def hashFloors():
    '''Creates a unique hash value for the state of the floors'''
    hash = 0
    for floor in FLOORS:
        for item in floor.items():
            local_hash = item.hash( floor.floor_num )
##            print item, item.id, local_hash
            hash |= item.hash( floor.floor_num )
    return hash

DEAD = 'DEAD'
VALID = 'VALID'
DONE = 'DONE'

class Move:
    UP = 1
    DOWN = -1
    DIR_STR = { UP : 'UP', DOWN : 'DOWN' }
    def __init__( self, direction, payload ):
        self.dir = direction
        self.payload = payload

    def __str__( self ):
        return '%s %s' % ( self.DIR_STR[ self.dir ], self.payload )

    def __repr__( self ):
        return str(self)

    def isReverse( self, m ):
        if ( m is None ): return False
        val = self.dir == -m.dir # opposite directions
        val = val and len( self.payload ) == len( m.payload )
        for item in self.payload:
            val = val and item in m.payload
        return val

def enumerateOptions( floor ):
    '''Creates a list of all possible moves.'''
##    print "Enumerating options", floor
    this_floor = FLOORS[ floor ]
##    print "\t", this_floor
    DIRS = []
    if ( floor < 3 ):
        DIRS.append(Move.UP)
    if ( floor > 0 ):
        DIRS.append(Move.DOWN)
    moves = []
    for d in DIRS:
##        print "DIR:", Move.DIR_STR[ d ]
        nbr = FLOORS[ floor + d ]
##        print "\tNbr:", nbr
        for i in xrange( len( this_floor ) ):
            item_i, f_i = this_floor.pop( [i] )    # is this floor valid if I remove it?
##            print "\t\tTesting", item_i
            if ( f_i.isValid() ):
##                print "\t\t\tFloor %d left valid - %s" % ( floor, f_i )
                if nbr.test( item_i ):
##                    print "\t\t\t\tFloor %d made valid" % ( nbr.floor_num )
                    moves.append( Move( d, item_i ) )
            for j in xrange( i + 1, len( this_floor ) ):
                items_ij, f_j = this_floor.pop( [i, j] )
##                print "\t\t\tTesting", items_ij
                if ( f_j.isValid() ):
##                    print "\t\t\t\tFloor %d left valid - %s" % ( floor, f_j )
                    if ( nbr.test( items_ij ) ):
##                        print "\t\t\t\t\tFloor %d made valid" % ( nbr.floor_num )
                        moves.append( Move( d, items_ij ) )
    return moves

def checkFloorState():
    '''Reports the state of the scenario'''
    if ( FLOORS[0].isEmpty() and FLOORS[1].isEmpty() and FLOORS[2].isEmpty() ):
        return DONE
    for floor in FLOORS:
        if not floor.isValid():
            return DEAD
    return VALID

def drawFloors(indent=''):
    print indent, '-----------------------------------------------------'
    print '\n'.join( map( lambda f: indent + " " + str(f), FLOORS[::-1] ) )
    print indent, '-----------------------------------------------------'

def applyMove( move, floor ):
    FLOORS[ floor ].remove( move.payload )
    FLOORS[ floor + move.dir ].append( move.payload )

def undoMove( move, floor ):
    FLOORS[ floor ].append( move.payload )
    FLOORS[ floor + move.dir ].remove( move.payload )

def findSolution( elevator, lastMove=None, depth=0, maxDepth=44 ):
    '''Evaluts a move and returns the number of moves required'''
    indent = '  ' * depth + '|'
##    print indent, "=============================================="
##    print indent, "findSolution( %d )" % ( elevator )
    if ( depth >= maxDepth ):
##        print indent, "MAXIMUM DEPTH"
        return np.inf
    moves = enumerateOptions( elevator )
    best = np.inf
##    print indent, "Move candidates:", moves
    for move in moves:
        # if I have multiple options, I can skip the reverse...if going back is the only option, take it.
##        print indent, "\t", move, 'depth %02d' % ( depth )
        if ( move.isReverse( lastMove ) ):
##            print indent, "\t\tOnly available move reverses the previous move - end of chain"
            continue
##        print indent, "\tBEFORE MOVE"
##        drawFloors(indent + '\t')
        applyMove( move, elevator ) # modify the floor state
        
        state = checkFloorState()
##        print indent, "\tMOVE APPLIED", state
##        drawFloors(indent + "\t")
        if ( state == DEAD ):
            pass
        elif ( state == DONE ):
            best = 1
        else:
            local_best = 1 + findSolution( elevator + move.dir, move, depth + 1 )
            best = min( local_best, best )
        undoMove( move, elevator )
    return best

def test():
    print "\nTEST 1 ==================="
    drawFloors()
##    print hashFloors()
##    print "State:", checkFloorState()
    if ( False ):
        moves = enumerateOptions( 2 )
        print '---MOVES---'
        for m in moves:
            print m
    else:
        HISTORY = set()
        count = findSolution(0)
        sys.stderr.write('COUNT: %s' % count )

def problem():
    print "\nProblem 1 ==================="
    with open( 'input.txt', 'r' ) as f:
        pass

if __name__ == '__main__':
    test()
    problem()