# My solution to the advent of code 2016 day 15 puzzle

import os
os.chdir(os.path.split(__file__)[0])
import time

def scramble( password, instructions ):
    for inst in instructions:
        inst = inst.strip().split()
        if ( inst[0] == 'swap' ):
            if ( inst[1] == 'position' ):
                X = int( inst[2] )
                Y = int( inst[5] )
                if ( X > Y ):   # x is always smaller
                    t = X
                    X = Y
                    Y = t
                # swap positions
                cX = password[ X ]
                cY = password[ Y ]
                password = password[:X] + cY + password[X+1:Y] + cX + password[Y+1:]
            elif ( inst[1] == 'letter' ):
                X = password.index( inst[2] )
                Y = password.index( inst[5] )
                if ( X > Y ):   # x is always smaller
                    t = X
                    X = Y
                    Y = t
                # swap positions
                cX = password[ X ]
                cY = password[ Y ]
                password = password[:X] + cY + password[X+1:Y] + cX + password[Y+1:]
            else:
                print "ERROR- unrecognized swap operation", ' '.join( inst )
        elif ( inst[0] == 'rotate' ):
            if ( inst[1] == 'based' ):
                c = inst[-1]
                idx = password.index(c)
                rotAmount = 1 + idx
                if ( idx >= 4 ):
                    rotAmount += 1
                rotAmount = rotAmount % len( password )
                password = password[-rotAmount:] + password[:-rotAmount]
            else:
                steps = int( inst[2] )
                steps = steps % len( password )
                if ( inst[1] == 'left' ):
                    password = password[steps:] + password[:steps]
                elif ( inst[1] == 'right' ):
                    password = password[-steps:] + password[:-steps]
                else:
                    print "ERROR - unrecognized rotate opration:", ' '.join( inst )
        elif ( inst[0] == 'reverse' ):
            start = int( inst[2] )
            stop = int( inst[4] )
            password = password[:start] + password[start:stop+1][::-1] + password[stop+1:]
        elif ( inst[0] == 'move' ):
            X = int( inst[2] )
            Y = int( inst[5] )
            cX = password[X]
            password = password[:X] + password[X+1:]
            password = password[:Y] + cX + password[Y:]
        else:
            print "ERROR - unrecognized opration:", ' '.join( inst )
    return password

def descramble( password, instructions ):
    for iStr in instructions[::-1]:
        inst = iStr.strip().split()
        if ( inst[0] == 'swap' ):
            # swapping is its own inverse
            if ( inst[1] == 'position' ):
                X = int( inst[2] )
                Y = int( inst[5] )
                if ( X > Y ):   # x is always smaller
                    t = X
                    X = Y
                    Y = t
                # swap positions
                cX = password[ X ]
                cY = password[ Y ]
                password = password[:X] + cY + password[X+1:Y] + cX + password[Y+1:]
            elif ( inst[1] == 'letter' ):
                X = password.index( inst[2] )
                Y = password.index( inst[5] )
                if ( X > Y ):   # x is always smaller
                    t = X
                    X = Y
                    Y = t
                # swap positions
                cX = password[ X ]
                cY = password[ Y ]
                password = password[:X] + cY + password[X+1:Y] + cX + password[Y+1:]
            else:
                print "ERROR- unrecognized swap operation", ' '.join( inst )
        elif ( inst[0] == 'rotate' ):
            if ( inst[1] == 'based' ):
                # This is *very* tricky.  I have to roll it back until the new state would map to the current state
                c = inst[-1]
                idx = password.index(c)
                leftRot = 1
                candidate = password[leftRot: ] + password[:leftRot]
                while ( password != scramble( candidate, [iStr] ) ):
                    leftRot += 1
                    candidate = password[leftRot: ] + password[:leftRot]
                password = candidate
            else:
                # rotate amounts is as simple as remapping word to direction - DONE
                steps = int( inst[2] )
                steps = steps % len( password )
                if ( inst[1] == 'right' ):
                    password = password[steps:] + password[:steps]
                elif ( inst[1] == 'left' ):
                    password = password[-steps:] + password[:-steps]
                else:
                    print "ERROR - unrecognized rotate opration:", ' '.join( inst )
        elif ( inst[0] == 'reverse' ):
            # reverse is its own inverse
            start = int( inst[2] )
            stop = int( inst[4] )
            password = password[:start] + password[start:stop+1][::-1] + password[stop+1:]
        elif ( inst[0] == 'move' ):
            # reverse move, grab the Yth part and put it at X - DONE
            X = int( inst[2] )
            Y = int( inst[5] )
            cY = password[Y]
            password = password[:Y] + password[Y+1:]
            password = password[:X] + cY + password[X:]
        else:
            print "ERROR - unrecognized opration:", ' '.join( inst )
    return password

def test():
    print "\nTEST 1 ==================="
    print scramble( 'abcdef', ['move position 2 to position 4']), 'abdecf'
    print scramble( 'abcdef', ['reverse positions 2 through 4']), 'abedcf'
    print scramble( 'abcdef', ['rotate based on position of letter b']), 'efabcd'
    print scramble( 'abcdef', ['rotate based on position of letter e']), 'abcdef'
    print scramble( 'abcdefg', ['rotate based on position of letter e']), 'bcdefga'
    print scramble( 'abcdefg', ['rotate right 3 steps']), 'efgabcd'
    print scramble( 'abcdefg', ['rotate left 3 steps']), 'defgabc'
    print scramble( 'abcdefg', ['swap letter b with letter f'] ), 'afcdebg'
    print scramble( 'abcdefg', ['swap position 4 with position 2'] ), 'abedcfg'

    print
    print scramble( 'abcde', ['swap position 4 with position 0',
                              'swap letter d with letter b',
                              'reverse positions 0 through 4',
                              'rotate left 1 step',
                              'move position 1 to position 4',
                              'move position 3 to position 0',
                              'rotate based on position of letter b',
                              'rotate based on position of letter d'] ), 'decab'

def test2():
    print "\nTEST 2 ======================="
    print descramble( 'abdecf', ['move position 2 to position 4']), 'abcdef'
    print descramble( 'abedcf', ['reverse positions 2 through 4']), 'abcdef'
    print descramble( 'efabcd', ['rotate based on position of letter b']), 'abcdef'
    print descramble( 'abcdef', ['rotate based on position of letter e']), 'abcdef'
    print descramble( 'bcdefga', ['rotate based on position of letter e']), ''
    print descramble( 'efgabcd', ['rotate right 3 steps']), 'abcdefg'
    print descramble( 'defgabc', ['rotate left 3 steps']), 'abcdefg'
    print descramble( 'afcdebg', ['swap letter b with letter f'] ), 'abcdefg'
    print descramble( 'abedcfg', ['swap position 4 with position 2'] ), 'abcdefg'

    print
    print descramble( 'decab', ['swap position 4 with position 0',
                              'swap letter d with letter b',
                              'reverse positions 0 through 4',
                              'rotate left 1 step',
                              'move position 1 to position 4',
                              'move position 3 to position 0',
                              'rotate based on position of letter b',
                              'rotate based on position of letter d'] ), 'abcde'

def problem():
    print "\nProblem 1 ==================="
    start = time.clock()
    with open( 'input.txt', 'r' ) as f:
        instructions = [ line.strip() for line in f.readlines() ]
    print scramble( 'abcdefgh', instructions )
    elapsed = time.clock() - start
    print "Took %f seconds" % elapsed
    
def problem2():
    print "\nProblem 2 ==================="
    start = time.clock()

    with open( 'input.txt', 'r' ) as f:
        instructions = [ line.strip() for line in f.readlines() ]
    print descramble( 'fbgdceah', instructions ), 'abcdefgh'

    elapsed = time.clock() - start
    print "Took %f seconds" % elapsed
    
if __name__ == '__main__':
    test()
    test2()
    problem()
    problem2()
    
