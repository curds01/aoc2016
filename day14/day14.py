# My solution to the advent of code 2016 day 13 puzzle
#   A crappy A* implementation

import os
os.chdir(os.path.split(__file__)[0])
import re
import numpy as np
from heapq import *
import md5

TRIPLE_RE = re.compile('.*?((?P<A>.)(?P=A)(?P=A))')

def getHex( hash, count ):
    hex = hash
    for i in xrange( count ):
        hex = md5.md5( hex ).hexdigest()
    return hex

def generateKeys( salt, stretchCount, targetCount ):
    i = 0
    count = 0
    salts = {}
    while ( count < targetCount ):
        hash = salt + '%d' % i
        if ( salts.has_key( hash ) ):
            hex = salts[ hash ]
        else:
            hex = getHex( hash, stretchCount + 1 )
            salts[hash] = hex
        m = TRIPLE_RE.match( hex )
        if ( m ):
            re_str = '.*?%s{5}' % m.group(2)
            five_re = re.compile(re_str )
            for j in xrange( i + 1, i + 1 + 1000 ):
                hash = salt + '%d' % j
                if ( salts.has_key( hash ) ):
                    hex = salts[ hash ]
                else:
                    hex = getHex( salt + '%d' % j, stretchCount + 1 )
                    salts[ hash ] = hex
                m = five_re.match( hex )
                if ( m ):
                    count += 1
                    print "Hash", count, salt, i
                    break
        i += 1

def test():
    print "\nTEST 1 ==================="
    salt = 'abc'
    generateKeys( salt, 0, 64 )
    
    
def problem():
    print "\nProblem 1 ==================="
    salt = 'qzyelonm'
    generateKeys( salt, 0, 64 )
    
    
def problem2():
    print "\nProblem 2 ==================="
    salt = 'qzyelonm'
    generateKeys( salt, 2016, 64 )

if __name__ == '__main__':
    test()
    problem()
    problem2()
    
