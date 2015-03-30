#!/usr/bin/env python2
# Util - functions that are used both by client and server
# PIR - Goldbergs Protocol
# CS 54701 Project- Craig West & Michael 

#TODO: do all of our multiplications need to be mod n?
#all coefficients in the created polynomials must be in Zn
#the polyEval function must produce outputs in Zn
#

from random import randint
import sys

#evaluate a given polynomial and x, to return the output y
def polyEval( poly ,  x):
    r = 0
    for idx, c in enumerate(poly):     
        if idx ==0:
            r = c
        else:
            r = r + (c *( x**idx))
    return r

#p = [1 ,  4,  6,  4]
#print polyEval(p, 3)

#matrix multiplication , where m1 is always a vector 
def matrixMult(m1,  m2):
    m1_c= len( m1)
    m2_r = len( m2)
    m2_c = len(m2[0])
    
    #check that matrix multiplication is allowed
    if m1_c != m2_r:
        return -1
    output = [ ]
    for r in xrange(0,m1_c):
        row = [ ]
        for c in xrange(0, m2_c):
            o = 0
            for t in xrange(0, m1_c):
               o = o + int(m1[t]) * int(m2[t][c])
            row.append(o)
        output.append(row)
        
    return output
    
    
#polynomial creation for shamir secret sharing  : deg = degree of polynomial, constant = the secret value , bound = max value for coefficients
#the poly returned is of the form [constant, x^3, x^2, x ] for a deg=3 polynomial . all values are coefficients
def createShamirPoly( deg,  constant,  bound):
    print " in create poly, passed:  deg "  + str(deg) + " constant " + str(constant) + "  bound " + str(bound)
    if int(deg)<0:
        print(" ERROR: Degree of polynomial requested < 0")
        sys.exit(1)
    output = [constant]
    for x in xrange(0, deg):
        output.append(randint(1, bound-1))
    return output
            
                

