# My solution to the advent of code 2016 day 7 puzzle

import os
os.chdir(os.path.split(__file__)[0])
import numpy as np
import re

RECT_RE = re.compile('rect ([0-9]+)x([0-9]+)')
ROT_ROW_RE = re.compile('rotate row y=([0-9]+) by ([0-9]+)')
ROT_COL_RE = re.compile('rotate column x=([0-9]+) by ([0-9]+)')

W = 50
H = 6
screen = np.zeros((H, W), dtype=np.bool)

def init():
    global screen
    screen[:, :] = False
    
def rect( a, b ):
    '''Turns on all of the pixels in a rectangle at the top-left of the
    screen which is A wide and B tall.'''
    global screen
    screen[ :b, :a ] = True

def rotate_row( a, b ):
    '''shifts all of the pixels in row A (0 is the top row) right by B
    pixels. Pixels that would fall off the right end appear at the left
    end of the row.'''
    b = b % W
    row = np.empty( W, dtype=np.bool )
    row[b:] = screen[ a, :(W-b)]
    row[:b] = screen[ a, W-b: ]
    screen[ a, : ] = row

def rotate_col( a, b ):
    '''shifts all of the pixels in column A (0 is the left column) down
    by B pixels. Pixels that would fall off the bottom appear at the top
    of the column.'''
    b = b % H
    col = np.empty( H, dtype=np.bool )
    col[b:] = screen[ :(H-b), a]
    col[:b] = screen[ H-b:, a ]
    screen[ :, a ] = col

def illuminated():
    global screen
    return screen.sum()

def printScreen():
    s = ''
    for row in screen:
        for c in row:
            if c:
                s += '#'
            else:
                s += ' '
        s += '\n'
    print s

def executeInstruction( inst ):
    global screen
    m = RECT_RE.match( inst )
    if ( m ):
        rect( int(m.group(1)), int(m.group(2)) )
    else:
        m = ROT_ROW_RE.match( inst )
        if ( m ):
            rotate_row( int(m.group(1)), int(m.group(2)) )
        else:
            m = ROT_COL_RE.match( inst )
            if ( m ):
                rotate_col( int(m.group(1)), int(m.group(2)) )
            else:
                print "Unrecotgnized instruction:", inst
                
    

def test():
    print "TEST 1 ==================="
    init()
    print "Starts with %d pixels lit" % ( illuminated() )
    inputs = (('rect 3x2', 6),
              ('rotate column x=1 by 1', 6),
              ('rotate row y=0 by 4', 6),
              ('rotate row y=1 by 1', 6)
              )
    for inst, count in inputs:
        printScreen()
        print inst
        executeInstruction( inst )
        if ( count == illuminated() ):
            print "Passed", inst
        else:
            print "Failed", inst
    printScreen()


def problem():
    print "Problem 1 ==================="
    init()
    with open( 'input.txt', 'r' ) as f:
        for line in f.xreadlines():
            executeInstruction( line.strip() )
    printScreen()
    print illuminated()

if __name__ == '__main__':
    test()
    problem()
    
