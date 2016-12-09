# My solution to the advent of code 2016 day 7 puzzle

import os
os.chdir(os.path.split(__file__)[0])
import numpy as np
import re

RE = re.compile( '(.*?)\(([0-9]+)x([0-9]+)\)(.*)')

def explodeString( s ):
    result = ''
    while ( s ):
        m = RE.match( s )
        if ( m == None ):
            result += s
            s = ''
        else:
            result += m.group(1)
            s = m.group(4)
            count = int(m.group(2))
            repeat = int(m.group(3))
            result += s[:count] * repeat
            s = s[count:]
    return result

def explodeString2( s ):
    result = 0
    while ( s ):
        m = RE.match( s )
        if ( m == None ):
            result += len( s )
            s = ''
        else:
            result += len( m.group(1) )
            s = m.group(4)
            count = int(m.group(2))
            repeat = int(m.group(3))
            result += explodeString2( s[:count] ) * repeat
            s = s[count:]
    return result


def test():
    print "TEST 1 ==================="
    inputs = (
               ('ADVENT', 'ADVENT'),
               ( 'A(1x5)BC', 'ABBBBBC' ),
               ( '(3x3)XYZ', 'XYZXYZXYZ' ),
               ( 'A(2x2)BCD(2x2)EFG', 'ABCBCDEFEFG' ),
               ('(6x1)(1x3)A' , '(1x3)A' ),
               ( 'X(8x2)(3x3)ABCY', 'X(3x3)ABC(3x3)ABCY' )
               )
    for input, expected in inputs:
        result = explodeString( input )
        if ( result == expected ):
            print "PASSED", input, result
        else:
            print "FAILED", input, result

def test2():
    print "TEST 1 ==================="
    inputs = (
               ('ADVENT', 6),
               ( 'A(1x5)BC', 7 ),
               ( '(3x3)XYZ', 9 ),
               ( 'X(8x2)(3x3)ABCY', len('XABCABCABCABCABCABCY') ),
               ('(27x12)(20x12)(13x14)(7x10)(1x12)A' , 241920 ),
               ( '(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN', 445 )
               )
    for input, expected in inputs:
        result = explodeString2( input )
        if ( result == expected ):
            print "PASSED", input, result
        else:
            print "FAILED", input, expected, result

def problem():
    print "Problem 1 ==================="
    with open( 'input.txt', 'r' ) as f:
        data = ''.join(map( lambda x: x.strip(), f.readlines()))
        result = explodeString( data )
        print len(result)
        
def problem2():
    print "Problem 2 ==================="
    with open( 'input.txt', 'r' ) as f:
        data = ''.join(map( lambda x: x.strip(), f.readlines()))
        result = explodeString2( data )
        print result

if __name__ == '__main__':
    test()
    problem()
    test2()
    problem2()
