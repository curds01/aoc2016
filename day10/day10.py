# My solution to the advent of code 2016 day 7 puzzle

import os
os.chdir(os.path.split(__file__)[0])
import numpy as np
import re
import sys

value_re = re.compile( 'value ([0-9]+) goes to bot ([0-9]+)')
give_re = re.compile('bot ([0-9]+) gives low to (bot|output) ([0-9]+) and high to (bot|output) ([0-9]+)')

bots = [ [] for x in xrange(255) ]
output = [[] for x in xrange(255) ]

def addToBot( bot, val ):
    if ( len( bots[ bot ] ) > 1 ):
        print "Robot %d already had two values", bots[bot]
        sys.exit()
    bots[bot].append( val )
    bots[bot].sort()

def addToOutput( bot, val ):
    output[bot].append( val )
    output[bot].sort()

def func( s ):
    '''evaluate an instruction'''
    m = value_re.match(s)
    if ( m ):
        bot = int( m.group(2) )
        val = int( m.group(1) )
        addToBot( bot, val )
    else:
        m = give_re.match(s)
        if ( m ):
            bot = int( m.group(1) )
            if (len( bots[bot] ) < 2 ):
                return False
            lowTgt = int( m.group(3) )
            highTgt = int( m.group(5) )
            vals = bots[bot]
            bots[bot] = []
            if ( m.group(2) == 'bot' ):
                addToBot( lowTgt, vals[0] )
            else:
                addToOutput( lowTgt, vals[0] )
            if ( m.group(4) == 'bot' ):
                addToBot( highTgt, vals[1] )
            else:
                addToOutput( highTgt, vals[1] )
        else:
            print "Couldn't parse instrution"
            sys.exit()
    return True

def test():
    print "\nTEST 1 ==================="
    inputs = ['value 5 goes to bot 2',
              'bot 2 gives low to bot 1 and high to bot 0',
              'value 3 goes to bot 1', 
              'bot 1 gives low to output 1 and high to bot 0', 
              'bot 0 gives low to output 2 and high to output 0', 
              'value 2 goes to bot 2', 
               ]
    queue = []
    readFromQueue = False
    while ( inputs or queue):
        newQueue = []
        for line in queue:
            consumed = func( line )
            if ( not consumed ):
                newQueue.append( line )
        queue = newQueue
        consumed = False
        while ( not consumed and inputs ):
            line = inputs.pop(0)
            consumed = func( line )
            if ( not consumed ):
                queue.append( line )
    print bots
    print output

def problem():
    print "\nProblem 1 ==================="
    value = -1
    with open( 'input.txt', 'r' ) as f:
        inputs = f.readlines()
    queue = []
    readFromQueue = False
    while ( inputs or queue):
        newQueue = []
        for line in queue:
            consumed = func( line )
            if ( not consumed ):
                newQueue.append( line )
            else:
                try:
                    value = bots.index( [17, 61] )
                except:
                    pass
        queue = newQueue
        consumed = False
        while ( not consumed and inputs ):
            line = inputs.pop(0)
            consumed = func( line )
            if ( not consumed ):
                queue.append( line )
            else:
                try:
                    value = bots.index( [17, 61] )
                except:
                    pass
    print 'Bot that processed:', value

if __name__ == '__main__':
##    test()
    problem()
    print 'Product of first three outputs:', output[0][0] * output[1][0] * output[2][0]
    