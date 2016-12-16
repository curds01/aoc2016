# My solution to the advent of code 2016 day 15 puzzle

import os
os.chdir(os.path.split(__file__)[0])
import re
import numpy as np

def makeChecksum( data ):
    sum = ''
    while ( True ):
        for i in xrange( 0, len( data ), 2 ):
            pair = data[i:i+2]
            if ( pair == '00' or pair == '11' ):
                sum += '1'
            else:
                sum += '0'
        if ( len( sum ) % 2 == 1 ):
            break
        else:
            data = sum
            sum = ''
    return sum

def getCode( seed, targetLen ):
    while len( seed ) < targetLen:
        seed = makeNoise( seed )
    data = seed[:targetLen]
    # make checksum
    checkSum = makeChecksum( data )
    return data, checkSum
    
def makeNoise( seed ):
    a = seed
    b = a[::-1]
    b = b.replace('0', 'x')
    b = b.replace( '1', '0' )
    b = b.replace('x', '1' )
    return a + '0' + b

def test():
    print "\nTEST 1 ==================="
    print makeNoise( '1' )
    print makeNoise('0')
    print makeNoise('11111')
    print makeNoise('111100001010')
    print 'checksum', makeChecksum('110010110100')
    
def problem():
    print "\nProblem 1 ==================="
    print getCode('01111010110010011', 272 )[1]
    
def problem2():
    print "\nProblem 2 ==================="
    print getCode('01111010110010011', 35651584 )[1]
    
if __name__ == '__main__':
    test()
    problem()
    problem2()
    
