# My solution to the advent of code 2016 day 15 puzzle

import os
os.chdir(os.path.split(__file__)[0])

def computeNextRow( currRow ):
    newRow = ['.' for c in currRow ]
    currRow = '.' + currRow + '.'
    for i in xrange( 1, len( currRow ) - 1):
        prev = currRow[i-1:i+2]
        if ( prev == '^^.' or
             prev == '.^^' or
             prev == '^..' or
             prev == '..^' ):
            newRow[ i - 1 ] = '^'
    return ''.join( newRow )

def countSafe( data ):
    count = 0
    for c in data:
        if c == '.':
            count += 1
    return count

def countSafeInRoom( firstRow, rowCount ):
    count = 0
    row = firstRow
    for i in xrange(rowCount):
        count += countSafe( row )
        row = computeNextRow( row )
    return count

def test():
    print "\nTEST 1 ==================="
    r = '..^^.'
    for i in xrange(3):
        print r
        r = computeNextRow( r )
    r = '.^^.^.^^^^'
    for i in xrange(10):
        print r
        r = computeNextRow( r )
    
def problem():
    print "\nProblem 1 ==================="
    with open( 'input.txt' ,'r' ) as f:
        row = ''.join( [line.strip() for line in f.readlines() ] )
        print countSafeInRoom( row, 40 )
    
def problem2():
    print "\nProblem 2 ==================="
    with open( 'input.txt' ,'r' ) as f:
        row = ''.join( [line.strip() for line in f.readlines() ] )
    
if __name__ == '__main__':
    test()
    problem()
    problem2()
    
