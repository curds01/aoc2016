# My solution to the advent of code 2016 day 15 puzzle

import os
os.chdir(os.path.split(__file__)[0])
import re
import numpy as np
import md5

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

def decodeDoors( code ):
    hash = md5.md5( code ).hexdigest()
    doorCodes = hash[:4]
    doorOpen = map( lambda x: x in 'bcdef', doorCodes )
    return doorOpen


def walk( start, code ):
    goal = (3, 3)
    q = [(start, code, 0)]
    def popSmallest():
        minDist = q[0][2]
        idx = 0
        for i, (p, c, d) in enumerate(q):
            if ( d < minDist ):
                minDist = d
                idx = i
        return q.pop( idx )
    while ( q ):
        p, c, dist = popSmallest()
        if ( p == goal ):
            return dist
        doors = decodeDoors( c )
        if ( doors ):
            if ( doors[UP] and p[1] > 0 ):
                newP = (p[0], p[1] - 1)
                q.append( ( newP, c + 'U', dist + 1 ) )
            if ( doors[DOWN] and p[1] < 3 ):
                newP = (p[0], p[1] + 1)
                q.append( ( newP, c + 'D', dist + 1 ) )
            if ( doors[LEFT] and p[0] > 0 ):
                newP = (p[0] - 1, p[1])
                q.append( ( newP, c + 'L', dist + 1 ) )
            if ( doors[RIGHT] and p[0] < 3 ):
                newP = (p[0] + 1, p[1])
                q.append( ( newP, c + 'R', dist + 1 ) )
    return -1

def walkLongest( start, code ):
    goal = (3, 3)
    longest = 0
    q = [(start, code, 0)]
    def popSmallest():
        minDist = q[0][2]
        idx = 0
        for i, (p, c, d) in enumerate(q):
            if ( d < minDist ):
                minDist = d
                idx = i
        return q.pop( idx )
    while ( q ):
        p, c, dist = popSmallest()
        if ( p == goal ):
            if ( dist > longest ):
                longest = dist
            continue
        doors = decodeDoors( c )
        if ( doors ):
            if ( doors[UP] and p[1] > 0 ):
                newP = (p[0], p[1] - 1)
                q.append( ( newP, c + 'U', dist + 1 ) )
            if ( doors[DOWN] and p[1] < 3 ):
                newP = (p[0], p[1] + 1)
                q.append( ( newP, c + 'D', dist + 1 ) )
            if ( doors[LEFT] and p[0] > 0 ):
                newP = (p[0] - 1, p[1])
                q.append( ( newP, c + 'L', dist + 1 ) )
            if ( doors[RIGHT] and p[0] < 3 ):
                newP = (p[0] + 1, p[1])
                q.append( ( newP, c + 'R', dist + 1 ) )
    return longest
        
    

def test():
    print "\nTEST 1 ==================="
    print walk((0, 0), 'ihgpwlah')
    print walk((0, 0), 'kglvqrro')
    print walk((0, 0), 'ulqzkmiv')
    print walkLongest((0,0),'ihgpwlah')
    
def problem():
    print "\nProblem 1 ==================="
    print walk((0, 0), 'yjjvjgan')
    
def problem2():
    print "\nProblem 2 ==================="
    print walkLongest((0,0),'yjjvjgan')
    
if __name__ == '__main__':
    test()
    problem()
    problem2()
    
