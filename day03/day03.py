# My solution to the advent of code 2016 day 3 puzzle

import os
os.chdir(os.path.split(__file__)[0])
import numpy as np

def testTriangle( x, y, z ):
    return x + y > z and x + z > y and y + z > x

def loadInput1( file ):
    with open( file, 'r' ) as f:
        tokens = map( lambda x: x.split(), f.readlines())
        return [ (int(x), int(y), int(z)) for x, y, z in tokens]

def loadInput2( file ):
    data = np.array(loadInput( file ))
    return np.reshape( data.T, (-1, 3) )

def problem():
    tris = loadInput1('input.txt')
    valid = 0
    for x, y, z in tris:
        if ( testTriangle( x, y, z ) ):
            valid += 1
    print "part 1:", valid #1032

    tris = loadInput2('input.txt')
    valid = 0
    for x, y, z in tris:
        if ( testTriangle( x, y, z ) ):
            valid += 1
    print 'part 2:', valid #1838

if __name__ == '__main__':
    problem()
    
