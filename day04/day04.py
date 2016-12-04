# My solution to the advent of code 2016 day 3 puzzle

import os
os.chdir(os.path.split(__file__)[0])
import numpy as np
import re

RE = re.compile('([a-z\-]+)\-([0-9]+)\[([a-z]+)')

def decodeRoom( room ):
    '''Given room, returns room, id, and checksum'''
    m = RE.match(room)
    checksum = m.group(3)
    code = m.group(1)
    id = int(m.group(2))
    return code, id, checksum

def validateChecksum( line ):
    code, id, checksum = decodeRoom( line )
    code = code.replace('-', '')
    counts = {}
    for c in code:
        if counts.has_key( c ):
            counts[c] += 1
        else:
            counts[c] = 1

    items = counts.items()
    def compare( t1, t2 ):
        res = cmp( t1[1], t2[1] )
        if ( res == 0 ):
            return cmp( t1[0], t2[0] )
        return -res
    items.sort(compare)
    testSum = ''.join( [ x[0] for x in items[:5] ] )
    if ( testSum == checksum ):
        return id
    return 0

def decrypt( room ):
    base = ord('a')
    code, id, checksum = decodeRoom( room )
    decode = ''
    for c in code:
        if ( c == '-' ):
            decode += ' '
        else:
            i = ord(c) - base
            i += id
            i %= 26
            c = chr( i + base )
            decode += c
    return decode, id

def loadInput( file ):
    with open( file, 'r' ) as f:
        # one string per line in the file
        return map( lambda x: x.strip(), f.readlines() )

def problem():
    data = loadInput('input.txt')
    sum = 0
    for line in data:
        sum += validateChecksum(line)
    print "Sum:", sum

def test():
    print "test:", validateChecksum('a-b-c-d-e-f-g-h-987[abcde]')
    print "test:", validateChecksum('not-a-real-room-404[oarel]')

def test2():
    print "decode:", decrypt('qzmt-zixmtkozy-ivhz-343[abcde]')

def problem2():
    data = loadInput('input.txt')
    for line in data:
        room, id = decrypt( line )
        if ( 'north' in room ):
            print room, id
    
if __name__ == '__main__':
    test()
    problem()
    test2()
    problem2()
    
