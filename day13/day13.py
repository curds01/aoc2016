# My solution to the advent of code 2016 day 13 puzzle
#   A crappy A* implementation

import os
os.chdir(os.path.split(__file__)[0])
import re
import numpy as np
from heapq import *

start = np.array( (1, 1), dtype=np.int )

def isWall( x, y, seed ):
    val = x * x + 3 * x + 2 * x * y + y + y * y + seed
    binVal = str(bin(val))[2:]
    count = 0
    for c in binVal:
        if c == '1': count += 1
    return count & 1 == 1

def drawOffice( X, Y, seed ):
    rowData = []
    for row in xrange( Y ):
        r = ''
        for col in xrange( X ):
            if ( isWall( col, row, seed ) ):
                r += '#'
            else:
                r += '.'
        rowData.append( r )
    print '\n'.join(rowData)

def computeH( p1, p2 ):
    dX = p1[0] - p2[0]
    dY = p1[1] - p2[1]
    return np.sqrt( dX * dX + dY * dY )

def neighbors( p ):
    '''Creates a list of neighbors of point p'''
    return [
            (p[0] - 1, p[1] ),
            (p[0], p[1] - 1),
            (p[0], p[1] + 1),
            (p[0] + 1, p[1] )
        ]

def aStar( start, goal, seed ):
    heap = []
    startH = computeH( start, goal )
    prev = None
    #               f, g, h,     pos
    heap = [ [startH, 0, startH, start ] ]
    visited = set()
    visited.add( start )
    prev = {}

    def g( pos ):
        '''get the g value for the given position'''
        for f, g, h, p in heap:
              if pos == p:
                  return g
        return None
    
    def isInHeap( pos ):
        for f, g, h, p in heap:
            if pos == p:
                return True
        return False

    def updatePos( pos, newG ):
        for data in heap:
            p = data[3]
            if ( p == pos ):
                f, g, h, p = data
                data[0] = newG + h
                data[1] = newG
    def popMin():
        minVal = heap[0][0]
        minIdx = 0
        for i, data in enumerate( heap[1:] ):
            f, g, h, pos = data
            if f < minVal:
                minVal = f
                minIdx = i + 1
        retVal = heap[minIdx]
        heap.pop(minIdx)
        return retVal
    
    found = False
    while ( heap ):
        f, g, h, pos = popMin()

        if ( pos == goal ):
            found = True
            break
        
        for testPos in neighbors(pos):
            if ( testPos[0] < 0 or testPos[1] < 0 ):
                # invalid region of board
                continue
            if ( isWall( testPos[0], testPos[1], seed ) ):
                continue
            if ( testPos in visited ):
                # already visited
                continue
            visited.add( testPos )
            tempG = g + 1 # the distance to any adjacent cell
            isOld = True
            if ( not isInHeap( testPos ) ):
                hVal = computeH( testPos, goal )
                heap.append( [1e7, 1e7, hVal, testPos ] )
                isOld = False
            elif ( tempG >= g( testPos ) ):
                continue
            prev[ testPos ] = pos
            updatePos( testPos, tempG )

    if ( found ):
        path = [ pos ]
        while prev.has_key( path[-1] ):
            path.append( prev[ path[-1] ] )
        return path[::-1]
    return []

def reach( start, seed, limit ):
    reachable = set()
    reachable.add( start )
    count = 1 # includes start
    visited = set()
    visited.add( start )
    heap = [ (nbr, 1) for nbr in neighbors( start ) if not isWall( nbr[0], nbr[1], seed ) ]
    def popMin():
        minVal = heap[0][1]
        minIdx = 0
        for i, data in enumerate( heap[1:] ):
            pos, dist = data
            if dist < minVal:
                minVal = dist
                minIdx = i + 1
        retVal = heap[minIdx]
        heap.pop(minIdx)
        return retVal
        
    while ( heap ):
        pos, dist = popMin()
        if ( dist > limit ):
            break
        if ( pos in visited ):
            continue
        if ( isWall( pos[0], pos[1], seed ) ):
            continue
        reachable.add( pos )
        visited.add( pos )
        count += 1
        heap.extend([ (nbr, dist + 1) for nbr in neighbors( pos ) if ( not isWall( nbr[0], nbr[1], seed ) and nbr[0] >= 0 and nbr[1] >= 0 ) ]) 
    return reachable

def problem2():
    print "\nProblem 2 ==================="
    reachable = reach( (1, 1), 1362, 50 )
    print reachable
    print len(reachable)
    
    
    
def test():
    print "\nTEST 1 ==================="
    drawOffice( 10, 10, 10 )
    path = aStar( (1, 1), (7, 4), 10 )
    print path
    print len(path) - 1
    
    
def problem():
    print "\nProblem 1 ==================="
    path = aStar( (1, 1), (31, 39), 1362 )
    print path
    print len(path) - 1

if __name__ == '__main__':
    test()
    problem()
    problem2()
    
