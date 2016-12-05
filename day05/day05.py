# My solution to the advent of code 2016 day 3 puzzle

import os
os.chdir(os.path.split(__file__)[0])
import md5

input = 'cxdnnyjw'

def findInterestingHash( base, start ):
    i = start
    while ( True ):
        test = base + '%d' % i
        hash = md5.md5( test ).hexdigest()
        if ( hash[:5] == '00000' ):
            return hash, i
        i += 1

def test():
    print findInterestingHash( 'abc', 0 )

def problem():
    password = ''
    start = 0
    for _ in xrange(8):
        val, start = findInterestingHash( input, start )
        start += 1
        password += val[5]
    print password

def problem2():
    password = [ None for _ in xrange(8) ]
    start = 0
    while None in password:
        val, start = findInterestingHash( input, start )
        print val
        start += 1
        pos = val[5]
        if ( pos in '01234567' ):
            print '\t', pos
            pos = int(pos)
            if ( password[ pos ] == None ):
                print '\t\t', val[6]
                password[pos] = val[6]
    print ''.join(password)
        
if __name__ == '__main__':
    test()
    problem()
    problem2()
    
