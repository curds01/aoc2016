# My solution to the advent of code 2016 day 11 puzzle

import os
os.chdir(os.path.split(__file__)[0])
import numpy as np
import re
import sys

COPY_RE = re.compile( 'cpy (.+) ([abcd])' )
INC_RE = re.compile( 'inc ([abcd])' )
DEC_RE = re.compile( 'dec ([abcd])' )
JNZ_RE = re.compile( 'jnz (.+) ([\-0-9]+)' )

class Instruction:
    def __init__( self, register ):
        self.reg = register

    def __repr__( self ):
        return str(self)

class Copy(Instruction):
    def __init__( self, value, register ):
        Instruction.__init__( self, register )
        self.val = value
        if ( self.val not in 'abcde' ):
            self.val = int( self.val )

    def __str__( self ):
        return 'copy %s %s' % ( self.val, self.reg )

    def eval( self, program ):
        '''Evaluates the instruction, returning the change to the pc.'''
        if ( isinstance(self.val, basestring) ):
            val = program.registers[ self.val ]
        else:
            val = self.val
        program.registers[ self.reg ] = val
        return 1

class Offset(Instruction):
    def __init__( self, value, register ):
        Instruction.__init__( self, register )
        self.val = int( value )

    def __str__( self ):
        if ( self.val > 0 ):
            return 'inc %s' % ( self.reg )
        else:
            return 'dec %s' % ( self.reg )

    def eval( self, program ):
        '''Evaluates the instruction, returning the change to the pc.'''
        program.registers[ self.reg ] += self.val
        return 1

class JumpIf:
    def __init__( self, testVal, offset ):
        self.testVal = testVal
        if ( self.testVal not in 'abcd' ):
            self.testVal = int( self.testVal )
        self.offset = int( offset )

    def __str__( self ):
        return 'jnz %s %s' % ( self.testVal, self.offset )

    def eval( self, program ):
        '''Evaluates the instruction, returning the change to the pc.'''
        testVal = self.testVal
        if ( isinstance( testVal, basestring) ):
            testVal = program.registers[testVal]
        if ( testVal != 0 ):
            return self.offset
        else:
            return 1

class Program:
    def __init__( self ):
        self.pc = 0
        self.registers = registers = { 'a':0, 'b':0, 'c':0, 'd':0 }
        self.instructions = []

    def setInstructions( self, commands ):
        '''A list of assmebly instructions'''
        success = True
        for line in commands:
            m = COPY_RE.match( line )
            if ( m ):
                self.instructions.append( Copy( m.group(1), m.group(2) ) )
                continue
            m = INC_RE.match( line )
            if ( m ):
                self.instructions.append( Offset( 1, m.group(1) ) )
                continue
            m = DEC_RE.match( line )
            if ( m ):
                self.instructions.append( Offset( -1, m.group(1) ) )
                continue
            m = JNZ_RE.match( line )
            if ( m ):
                self.instructions.append( JumpIf( m.group(1), m.group(2) ) )
                continue
            print 'Failed to parse:', line
            success = False
        return success

    def regStr( self ):
        return '| %d | %d | %d | %d |' % ( self.registers['a'],
                                           self.registers['b'],
                                           self.registers['c'],
                                           self.registers['d'] )

    def run( self ):
        iCount = len( self.instructions )
        while ( self.pc < iCount ):
##            print self.pc, self.instructions[ self.pc ]
            self.pc += self.instructions[ self.pc ].eval( self )
##            print '\t', self.regStr()

    
def test():
    print "\nTEST 1 ==================="
    instructions = '''cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a'''.split('\n')
    program = Program()
    program.setInstructions( instructions )
    program.run()
    print program.registers['a']

def problem():
    print "\nProblem 1 ==================="
    with open( 'input.txt', 'r' ) as f:
        program = Program()
        if ( program.setInstructions( f.readlines() ) ):
            program.run()
            print program.registers['a']

def problem2():
    print "\nProblem 2 ==================="
    with open( 'input.txt', 'r' ) as f:
        program = Program()
        program.registers['c'] = 1
        if ( program.setInstructions( f.readlines() ) ):
            program.run()
            print program.registers['a']
    
if __name__ == '__main__':
    test()
    problem()
    problem2()
    