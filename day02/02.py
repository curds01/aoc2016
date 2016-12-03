# move around keypad
#
# A button is a described as a set of offsets from the previous button:
#   ULDR
# Any move that takes me off the pad is ignored
# For the first number, the implicit "previous" number is 5.

# Keypad like
#   1 2 3
#   4 5 6
#   7 8 9
# Where 7 is at (0,0), and 3 is at (2, 2)

import os
os.chdir(os.path.split(__file__)[0])


VALUE = {(0, 0) : '7',
         (1, 0) : '8',
         (2, 0 ) : '9',
         (0, 1 ) : '4',
         (1, 1) : '5',
         (2, 1) : '6',
         (0, 2) : '1',
         (1, 2) : '2',
         (2, 2) : '3'
         }

def clamp( minVal, maxVal, testVal ):
    if ( testVal < minVal ): return minVal
    elif ( testVal > maxVal ): return maxVal
    else: return testVal

class KeyPos:
    '''Logic for evaluating a key position for the first problem'''
    FIVE = KeyPos(1, 1)
    def __init__( self, x, y ):
        self.x = x
        self.y = y

    def getValue( self ):
        return VALUE[ self.tuple() ]
    
    def __add__( self, a ):
        return KeyPos( clamp( 0, 2, self.x + a.x ), clamp( 0, 2, self.y + a.y ) )

    def __str__( self ):
        v = self.getValue()
        return "(%d, %d) = %s" % ( self.x, self.y, self.getValue() )

    def tuple( self ):
        return (self.x, self.y)

#     1
#   2 3 4
# 5 6 7 8 9
#   A B C
#     D
#
# Origin at 7
VALUE2 = {(0, 2): '1',
          (-1, 1) : '2',
          (0, 1) : '3',
          (1, 1) : '4',
          (-2, 0) : '5',
          (-1, 0) : '6',
          (0, 0) : '7',
          (1, 0) : '8',
          (2, 0 ) : '9',
          (-1, -1): 'A',
          (0, -1) : 'B',
          (1, -1) : 'C',
          (0, -2) : 'D'
          }

class KeyPos2( KeyPos ):
    '''The key position logic for problem 2'''
    FIVE = KeyPos2(-2, 0)
    def getValue( self ):
        return VALUE2[ self.tuple() ]
    
    def __add__( self, a ):
        # clamp row based on which column, and clamp column based on row
        newX = self.x + a.x
        newY = self.y + a.y
        minX = -2 + abs(self.y)
        maxX = -minX
        minY = -2 + abs(self.x)
        maxY = -minY
        return KeyPos2( clamp( minX, maxX, newX), clamp( minY, maxY, newY ) )


OFFSETS = { 'U':KeyPos(0, 1),
            'D':KeyPos(0, -1),
            'L':KeyPos(-1, 0),
            'R':KeyPos(1, 0)
            }
    
class KeyOffset:
    '''Definition of the offset for a single key'''
    def __init__( self, sequence ):
        self.sequence = sequence

    def getFinalKey( self, prevKey ):
        '''Evaluates the KeyOffset from previous to final to get final key'''
        currKey = prevKey
        for d in self.sequence:
            currKey = currKey + OFFSETS[d]
        return currKey

def getCode( keyOffsets, KeyType ):
    '''Given a sequence of key offsets, determines the code.'''
    code = ''
    prevKey = KeyType.FIVE
    for keyOffset in keyOffsets:
        prevKey = keyOffset.getFinalKey( prevKey )
        code += prevKey.getValue()
    print code

def getKeyOffsets( text ):
    return map( lambda x: KeyOffset( x.strip() ), text.split('\n') )
                
def test():
    code = '''ULL
    RRDDD
    LURDL
    UUUUD'''
    getCode( getKeyOffsets(code), KeyPos )
    getCode( getKeyOffsets(code), KeyPos2 )

def problem():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        code = ''.join(lines)
        getCode( getKeyOffsets(code), KeyPos )
        getCode( getKeyOffsets(code), KeyPos2 )

if __name__ == '__main__':
##    test()
    problem()
    
        