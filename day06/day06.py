# My solution to the advent of code 2016 day 3 puzzle

import os
os.chdir(os.path.split(__file__)[0])

testData = '''eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar'''

def mostFrequent( codes ):
    counts = [ {} for c in codes[0] ]
    for code in codes:
        for i, c in enumerate( code ):
            if ( counts[i].has_key( c ) ):
                counts[i][c] += 1
            else:
                counts[i][c] = 1
    values = [ [None, 0] for c in codes[0] ]
    for i in xrange( len(codes[0]) ):
        for key, value in counts[i].items():
            if value > values[i][1]:
                values[i][0] = key
                values[i][1] = value
    return ''.join( map( lambda x: x[0], values ) )

def leastFrequent( codes ):
    counts = [ {} for c in codes[0] ]
    for code in codes:
        for i, c in enumerate( code ):
            if ( counts[i].has_key( c ) ):
                counts[i][c] += 1
            else:
                counts[i][c] = 1
    values = [ [None, len(codes)] for c in codes[0] ]
    for i in xrange( len(codes[0]) ):
        for key, value in counts[i].items():
            if value < values[i][1]:
                values[i][0] = key
                values[i][1] = value
    return ''.join( map( lambda x: x[0], values ) )

def test():
    print mostFrequent(testData.split('\n'))

def problem():
    with open( 'input.txt', 'r' ) as f:
        lines = map( lambda x: x.strip(), f.readlines() )
    print mostFrequent( lines )
def problem2():
    with open( 'input.txt', 'r' ) as f:
        lines = map( lambda x: x.strip(), f.readlines() )
    print leastFrequent( lines )
        
if __name__ == '__main__':
    test()
    problem()
    problem2()
    
