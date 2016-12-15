# My solution to the advent of code 2016 day 15 puzzle

import os
os.chdir(os.path.split(__file__)[0])
import re
import numpy as np

class Disk:
    def __init__( self, base, stride ):
        '''aligned if ( t + self.base ) % self.stride == zero'''
        self.base = base
        self.stride = stride

    def aligned( self, t ):
        return ( t + self.base ) % self.stride == 0

def findAgreement( disks ):
    print "Search %d disks" % len( disks)
    for i, d in enumerate( disks ):
        print "Disc #%d has %d positions; at time=0, it is at position %d" % ( i + 1, d.stride, d.base - i - 1)
    t = 0
    aligned = False
    while ( True ):
        if ( all( d.aligned( t ) for d in disks ) ):
            return t
        t += 1

def test():
    print "\nTEST 1 ==================="
    disks = [ Disk(5, 5),
              Disk(3, 2)
              ]
    t = findAgreement( disks )
    print "Earliest time", t
    
    
def problem():
    print "\nProblem 1 ==================="
    disks = [ Disk( 6, 17),
              Disk( 10, 19),
              Disk( 4, 7),
              Disk( 11, 13),
              Disk( 6, 5),
              Disk( 6, 3 )
              ]
    t = findAgreement( disks )
    print "Earliest time", t
    
def problem2():
    print "\nProblem 2 ==================="
    disks = [ Disk( 6, 17),
              Disk( 10, 19),
              Disk( 4, 7),
              Disk( 11, 13),
              Disk( 6, 5),
              Disk( 6, 3 ),
              Disk( 7, 11 )
              ]
    t = findAgreement( disks )
    print "Earliest time", t
    
if __name__ == '__main__':
    test()
    problem()
    problem2()
    
