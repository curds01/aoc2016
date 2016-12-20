# My solution to the advent of code 2016 day 15 puzzle

import os
os.chdir(os.path.split(__file__)[0])
import time

def badRanges( ranges ):
    # sort into monotonically increasing intervals
    ranges = [ [int(x[0]), int(x[1]) ] for x in [ y.split('-') for y in ranges] ]
    ranges.sort()

    # collapse overlapping intervals
    i = 0
    while ( i < len( ranges ) - 1 ):
        l, u = ranges[i]
        if u >= ranges[i + 1][0] - 1:
            ranges[i][1] = max( ranges[i][1], ranges[i + 1][1] )
            ranges.pop( i + 1 )
        else:
            i += 1
    return ranges

def lowestVal( ranges ):
    invalid = badRanges( ranges )
    
    retVal = 0
    i = 0
    while ( i < len( invalid ) and retVal >= invalid[i][0] ):
        retVal = max( retVal, invalid[i][1] + 1 )
        i += 1
            
    return retVal

def validCount( ranges ):
    invalid = badRanges( ranges )
    
    valid = []
    count = 0
    if ( invalid[0][0] > 0 ):
        valid.append( (0, invalid[0][0] - 1) )
        count = invalid[0][0]
    for i, (l, u) in enumerate( invalid[:-1] ):
        valid.append( ( u + 1, invalid[i + 1][0] - 1 ) )
        count += invalid[i + 1][0] - 1 - ( u + 1 ) + 1
    count += 0xFFFFFFFF - invalid[-1][1]
    return count

def test():
    print "\nTEST 1 ==================="
    print lowestVal( ['0-1', '3-5'] ), 2
    print lowestVal( ['0-1', '3-5', '4-5' ] ), 2
    print lowestVal( ['0-1', '4-6', '3-7' ] ), 2
    print lowestVal( ['0-1', '4-6', '2-7' ] ), 8
    print lowestVal( ['0-1', '4-6', '1-41' ] ), 42
    
def problem():
    print "\nProblem 1 ==================="
    start = time.clock()
    with open('input.txt', 'r' ) as f:
        ranges = [ line.strip() for line in f.readlines() ]
    print lowestVal( ranges )


    elapsed = time.clock() - start
    print "Took %f seconds" % elapsed
    
def problem2():
    print "\nProblem 2 ==================="
    start = time.clock()
    
    with open('input.txt', 'r' ) as f:
        ranges = [ line.strip() for line in f.readlines() ]
    print validCount( ranges )

    elapsed = time.clock() - start
    print "Took %f seconds" % elapsed
    
if __name__ == '__main__':
    test()
    problem()
    problem2()
    
