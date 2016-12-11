import numpy as np


# Principles
#   Moving a G-M *matched* pair is *always* safe
#   Moving a M is only safe onto an empty floor, or a floor with nothing but M
#   Moving M-M has same constraints as M
#   Moving a G is safe onto an empty floor, a floor with only G, or a floor where all M's
#       are matched with their G's
#   Moving G-G is has same constraints as G
#   It is *never* safe to move an unmatched pair (either they are leaving an invalid state
#       -- impossible -- or they are moving into an invalid state -- not allowed.
#


# State is encoded as an integer
#
#  MN GN ... M2 G2 M1 G1 M0 G0 E
#   Each symbol is a 2-bit value (0-3, representing the floor it is on)
#
pairCount = 0

def addPair( mFloor, gFloor, state ):
    '''Adds an item pair to the state.

    @param      mFloor      The floor (1-4) the microchip is on.
    @param      gFloor      The floor (1-4] the generator is on.
    '''
    global pairCount
    gOffset = (pairCount * 2 + 1) * 2
    mOffset = gOffset + 2
    pairCount += 1
    state = state | (((gFloor - 1) & 3) << gOffset ) | (((mFloor - 1) & 3) << mOffset )
    return state

def nameForItem( i ):
    '''Returns the name of the ith item'''
    pair = ( i - 1 ) / 2
    letter = chr( ord('A') + pair )
    if ( i % 2 == 0 ):
        return letter + 'M'
    else:
        return letter + 'G'
    
def drawState(state, prefix=''):
    '''Draws the state to the console'''
    floors = [ prefix + 'F%d' % (i + 1) for i in xrange(4) ]  # four floors
    def appendSymbol( f, symbol ):
        for i, floor in enumerate(floors):
            icon = '.'
            if ( i == f ):
                icon = symbol
            floors[i] = floor + '{0:>3}'.format(icon)
    appendSymbol( state & 3, 'E' )
    val = state >> 2
    for p in xrange( pairCount ):
        letter = chr( ord('A') + p )
        gFloor = val & 3
        val = val >> 2
        mFloor = val & 3
        val = val >> 2
        appendSymbol( gFloor, letter + 'G' )
        appendSymbol( mFloor, letter + 'M' )
    print '\n'.join(floors[::-1])

class Move:
    UP = 1
    DOWN = -1
    DIR_STR = { UP : 'UP', DOWN : 'DOWN' }
    def __init__( self, direction, payload ):
        '''Constructor

        @param  direction   An int {-1, 1} the offset to the elevator (up or down.)
        @param  payload     A list of ints (at most 2), each > 0.  It represents the 
                            nth item in the state (where the elevator is the 0th item).
        '''
        self.dir = direction
        self.payload = payload

    def __str__( self ):
        return '%s %s' % ( self.DIR_STR[ self.dir ], self.payload )

    def __repr__( self ):
        return str(self)

def items( state, floor ):
    '''Counts the number of items on this floor'''
    items = []
    val = state >> 2
    for i in xrange( pairCount * 2 ):
        if ( val & 3 == floor ):
            items.append( i + 1 )
        val = val >> 2
    return items

def moveItem( state, item, dir ):
    '''Creates a new state instance by moving the ith item in the given direction'''
    offset = item * 2
    currFloor = ( state >> offset ) & 3
    if ( currFloor != state & 3 ):
        print "Trying to move an element that is *not* on the same floor as the elevator."
        sys.exit(1)
    newFloor = currFloor + dir
    state = (state & ~(3 << offset)) | newFloor << offset
    return state

def isValid( state ):
    '''Reports if the state is valid'''
    unprotected = False
    unProtectedChipRows = set()
    genRows = set()
    val = state >> 2
    for pair in xrange(pairCount):
        gRow = val & 3
        mRow = (val >> 2) & 3
        val = val >> 4
        genRows.add( gRow )
        if ( gRow != mRow ):
            unProtectedChipRows.add( mRow )
    return len( genRows.intersection( unProtectedChipRows ) ) == 0

def findMoves( state ):
##    print "Enumerating options - floor", state & 3
    DIRS = []
    floor = state & 3
    if ( floor < 3 ):
        DIRS.append(Move.UP)
    if ( floor > 0 ):
        DIRS.append(Move.DOWN)
    moves = []
    for d in DIRS:
##        print "DIR:", Move.DIR_STR[ d ]
        floor_items = items( state, floor )
##        print "\tItems on floor %d: %s"% ( floor, floor_items )
        for i, item_i in enumerate( floor_items ):
            state_i = moveItem( state, item_i, d )
##            print "\t\tTesting", item_i, nameForItem(item_i)
            if ( isValid( state_i ) ):
##                print "\t\t\tValid state results, adding the move"
                moves.append( Move( d, [item_i] ) )
            for item_j in floor_items[i+1: ]:
                state_ij = moveItem( state_i, item_j, d )
##                print "\t\t\tTesting", item_j, nameForItem(item_j)
                if ( isValid(state_ij) ):
##                    print "\t\t\t\tValid state results, adding the move"
                    moves.append( Move( d, [item_i, item_j] ) )
    return moves

def applyMove( state, move ):
    # move the elevator
    eFloor = state & 3
    for item in move.payload:
        state = moveItem(state, item, move.dir )
    # dir should always be {1, -1} and be defined such that the lower 2 bits
    #   are always in the range [0, 3]
    state += move.dir   
    return state

def explore( initState, finalState ):
    '''Given an initial state and final state, explores the space to find the shortest
    path between states.
    '''
    costs = {initState:0}  #mapping from state to cost to initState
    moves = findMoves( initState )
    print moves
    def prioritize( a, b ):
        '''Sort algoritm to maintain the queue as a priority queue'''
        return cmp( a[1], b[1] )
    queue = [ (applyMove( initState, move ), 1) for move in moves ]
##    count = 0
##    dupe = 0
    while queue:
        testState, testCost = queue.pop(0)
##        count += 1
##        if ( count % 1000 == 0 ):
##            print "Tested %d configurations with a queue of %d" % ( count, len(queue))
        if ( testState == finalState ):
            return testCost
        if ( costs.has_key( testState ) ):
##            dupe += 1
##            if ( dupe % 1000 == 0 ):
##                print "\tEncountered %d dupes" % dupe
            # Already encountered this state
            if ( testCost < costs[ testState ] ):
                print '!!! Found smaller cost later !!!'
                sys.exit(1)
        else:
            costs[ testState ] = testCost
            moves = findMoves( testState )
            qCandidates = [ (applyMove( testState, move ), testCost + 1) for move in moves ]
            queue.extend( filter( lambda x: not costs.has_key( x[0] ), qCandidates ) )
            queue.sort( prioritize )
    print "Exited without finding a solution"
    return np.inf
        

def finalState():
    state = 3
    for i in xrange(pairCount):
        mOffset = (i * 2 + 1) * 2
        gOffset = mOffset + 2
        state = state | (3 << gOffset ) | (3 << mOffset )
    return state

def initProblem():
    state = 0
    state = addPair(1, 1, state)   # thulium
    state = addPair(2, 1, state)   # plutonium
    state = addPair(2, 1, state)   # strontium
    state = addPair(3, 3, state)   # promethium
    state = addPair(3, 3, state)   #ruthenium
    return state

def initProblem2():
    state = initProblem()
    state = addPair( 1, 1, state ) #elerium
    state = addPair( 1, 1, state ) # dilithium
    return state

def initTest():
    state = 0
    state = addPair( 1, 2, state ) # hydrogen
    state = addPair( 1, 3, state ) # lithium
    return state

if __name__ == '__main__':
    if ( False ):
        print "PROBLEM 1"
        state = initProblem()
    elif ( True ):
        print "PROBLEM 2"
        state = initProblem2()
    else:
        print "TEST"
        state = initTest()
    final = finalState()
    print 'Initial state'
    drawState(state, '  |')
    # test doing moves
    if ( False ):
        moves = [ Move( 1, [2, 4] ),
                  Move( -1, [2, 4] ),
                  Move( 1, [2] ),
                  Move( 1, [1, 2] ),
                  Move( -1, [2] ),
                  Move( -1, [2] ),
                  Move( 1, [ 2, 4] ),
                  Move( 1, [ 2, 4] ),
                  Move( 1, [ 2, 4] ),
                  Move( -1, [2] ),
                  Move( 1, [ 1, 3] ),
                  Move( -1, [1] ),
                  Move( 1, [ 1, 2] ),
                  ]
        for m in moves:
            state = applyMove( state, m )
            print '\n', m, "is valid:", isValid(state)
            drawState( state )
    # test queries on state
    if ( False ):
        for i in xrange(4 ):
            print "Items on %d:" % ( i + 1), items( state, i )
    # test move list
    if ( False ):
        moves = findMoves( state )
        print moves
    if ( True ):
        print "Targeted final state"
        drawState(final, '  |')
        cost = explore( final, state )
        print "Minimum cost:", cost
        
    
    
