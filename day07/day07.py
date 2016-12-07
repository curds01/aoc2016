# My solution to the advent of code 2016 day 7 puzzle

import os
os.chdir(os.path.split(__file__)[0])
import re

BAD_XYYX_PATTERN =  '\[[a-z]*(?P<xyyx>(?P<A>[a-z])(?P<B>[^(?P=A)])(?P=B)(?P=A))[a-z]*\]'
GOOD_XYYX_PATTERN =  '[^\[]*(?P<xyyx>(?P<A>[a-z])(?P<B>[^(?P=A)])(?P=B)(?P=A))[^\]]*'
BAD_XYYX = re.compile( BAD_XYYX_PATTERN )
GOOD_XYYX = re.compile( GOOD_XYYX_PATTERN )

def supportsTLS_RE( ip ):
    # couldn't get this to work; the reg ex would match 'aaaa'.
    m = BAD_XYYX.search(ip)
    has_bad = False
    has_good = False
    if ( m ):
        has_bad = True

    m = GOOD_XYYX.search(ip)
    if ( m ):
        has_good = True
    return has_good and not has_bad

def supportsTLS( ip ):
    '''Searches for abba strings without [abba] strings.'''
    stack = []
    height = 0
    hasOutside = False
    hasInside = False
    invalid = False
    for c in ip:
        if ( c == '[' ):
            stack = []
            invalid = True
        elif ( c == ']' ):
            stack = []
            invalid = False
        else:
            height = len( stack )
            if ( height == 0 ):
                stack.append( c )
            elif ( height == 1 ):
                if ( stack[0] != c ):
                    stack.append( c )
            elif ( height == 2 ):
                if ( stack[0] == stack[1] ):
                    print "ERROR with stack of height 2 on", ip
                if ( stack[-1] == c ):
                    stack.append( c )
                else:
                    stack = [stack[-1], c]
            elif ( height == 3 ):
                if ( stack[0] == stack[1] or stack[0] == stack[2] or stack[1] != stack[2] ):
                    print "ERROR with stack of height 3 on", ip
                if ( stack[0] == c ):
                    if ( invalid ):
                        return False
                    else:
                        hasInside = True
                    stack  = []
                else:
                    if ( stack[-1] == c ):
                        stack = [c]
                    else:
                        stack = [stack[-1], c]
    return hasInside


def supportsSSL( ip ):
    '''Searches for abba strings without [abba] strings.'''
    stack = []
    height = 0
    outsides = []
    insides = []
    invalid = False
    for c in ip:
        if ( c == '[' ):
            stack = []
            invalid = True
        elif ( c == ']' ):
            stack = []
            invalid = False
        else:
            height = len( stack )
            if ( height == 0 ):
                stack.append( c )
            elif ( height == 1 ):
                if ( stack[0] != c ):
                    stack.append( c )
            elif ( height == 2 ):
                if ( stack[0] == stack[1] ):
                    print "ERROR with stack of height 2 on", ip
                if ( stack[0] == c ):
                    code = ''.join( stack + [c] )
                    if ( invalid ):
                        outsides.append( code )
                    else:
                        insides.append( code )
                if ( stack[-1] != c ):
                    stack = [stack[-1], c]
                else:
                    stack = [c]
    for aba in insides:
        bab = aba[1:] + aba[1]
        if ( bab in outsides ):
            return True
    return False

def test():
    print "TEST 1 ==================="
    inputs = (('abba[mnop]qrst', True),
              ('abcd[bddb]xyyx', False),
              ('aaaa[qwer]tyui', False),
              ('ioxxoj[asdfgh]zxcvbn', True))
    for val, result in inputs:
        if ( supportsTLS( val ) != result ):
            print "Failed:", val
        else:
            print "Passed:", val


def test2():
    print "TEST 2 ==================="
    inputs = (('aba[bab]xyz', True),
              ('xyx[xyx]xyx', False),
              ('aaa[kek]eke', True),
              ('zazbz[bzb]cdb', True),)
    for val, result in inputs:
        if ( supportsSSL( val ) != result ):
            print "Failed:", val
        else:
            print "Passed:", val

def problem():
    print "Problem 1 ==================="
    count = 0
    with open( 'input.txt', 'r' ) as f:
        for line in f.xreadlines():
            if ( supportsTLS( line.strip() ) ):
                count += 1
    print count

def problem2():
    print "Problem 2 ==================="
    count = 0
    with open( 'input.txt', 'r' ) as f:
        for line in f.xreadlines():
            if ( supportsSSL( line.strip() ) ):
                count += 1
    print count

if __name__ == '__main__':
    test()
    test2()
    problem()
    problem2()
    
