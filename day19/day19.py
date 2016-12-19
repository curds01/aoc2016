# My solution to the advent of code 2016 day 15 puzzle

import os
os.chdir(os.path.split(__file__)[0])
import time

def movePresents( elfCount ):
    elves = [ i + 1 for i in xrange( elfCount ) ]
    idx = 0
    eCount = elfCount
    start = time.clock()
    while ( eCount > 1 ):
        if ( eCount % 100000 == 0 ): print eCount, (elfCount - eCount) / (time.clock() - start )
        killElf = ( idx + eCount / 2) % eCount
##        print "Elf %d kills %d" % ( elves[idx], elves[killElf] ), elves
        elves.pop( killElf )
        eCount -= 1
        if ( killElf > idx ):
            idx += 1
        if ( idx >= eCount ):
            idx = 0
    return elves[0]

def reduce( number ):
    jump = 2
    leading = 1
    while ( number > 1 ):
        remainder = number & 1
        if ( remainder ):
            # delete first and inset
            leading += jump
        jump = jump << 1
        number = number >> 1
    return leading

def test():
    print "\nTEST 1 ==================="
    print reduce( 5 )
    
def problem():
    print "\nProblem 1 ==================="
    start = time.clock()
    print reduce( 3005290 )
    lap = time.clock()
    print "Reduce took %f seconds" % ( lap - start )
    
def problem2():
    print "\nProblem 2 ==================="
    start = time.clock()
    print movePresents( 3005290 )
    end = time.clock()
    print "move took %f seconds" % ( end - start )
    
if __name__ == '__main__':
    test()
    problem()
    problem2()
    
