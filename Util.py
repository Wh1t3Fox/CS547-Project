#!/usr/bin/env python2
# Util - functions that are used both by client and server
# PIR - Goldbergs Protocol
# CS 54701 Project- Craig West & Michael 

from random import randint
import sys

#evaluate a given polynomial and x, to return the output y
def polyEval( poly ,  x ,   mod):
    r = 0
    for idx, c in enumerate(poly):     
        if idx ==0:
            r = c
        else:
            r = r + (c *( x**idx))
    return r % mod

#p = [1 ,  4,  6,  4]
#print polyEval(p, 3)

#matrix multiplication , where m1 is always a vector 
def matrixMult(m1,  m2,  mod):
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
            row.append((o % mod))
    return row
    
    
#polynomial creation for shamir secret sharing  : deg = degree of polynomial, constant = the secret value , bound = max value for coefficients
#the poly returned is of the form [constant, x^3, x^2, x ] for a deg=3 polynomial . all values are coefficients
def createShamirPoly( deg,  constant,  bound):
    #print " in create poly, passed:  deg "  + str(deg) + " constant " + str(constant) + "  bound " + str(bound)
    if int(deg)<0:
        print(" ERROR: Degree of polynomial requested < 0")
        sys.exit(1)
    output = [constant]
    for x in xrange(0, deg-1):    #this originally had just "deg" but this was wrong it was created polynomials 1 degree bigger than needed
        output.append(randint(1, bound-1))
    return output
            
                
#does lagrange interpolation for set of points, but is tweaked to quickly only compute the intercept value of the polynomial
#used only for shamir secret reformulation
def fastLagrangeInter_interceptOnly(points):
    num_points = len(points)
    f = 0 
    for idx, point in enumerate(points):
        L = 1
       # print " removed point is:" + str(point)
        for idx2 in xrange(num_points):
            if (idx2 !=idx):
                #print "point on: " + str(points[idx2][0]) + "," + str(points[idx2][1])
                #print " doing: " + str(L) + " * (-" + str(points[idx2][0]) + " ) / (" + str(point[0]) + "- " + str(points[idx2][0]) + " )"
                L = L * (-points[idx2][0]/(point[0] -points[idx2][0]))
                #print " L = " + str(L)
        #print " f="  + str(f) + "+( " + str(L) + "*" +str(point[1]) + ")"
        f = f + (L * point[1]) 
    return f
