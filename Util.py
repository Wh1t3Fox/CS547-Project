#!/usr/bin/env python2
# Util - functions that are used both by client and server
# PIR - Goldbergs Protocol
# CS 54701 Project- Craig West & Michael



from random import randint
import sys

COLORS = {
    'HEADER' : '\033[95m',
    'OKBLUE' : '\033[94m',
    'OKGREEN' : '\033[92m',
    'WARNING' : '\033[93m',
    'FAIL' : '\033[91m',
    'ENDC' : '\033[0m',
    'BOLD' : '\033[1m',
    'UNDERLINE' : '\033[4m'
}


#evaluate a given polynomial and x, to return the output y
def polyEval( poly ,  x ,   mod):
    r = 0
    for idx, c in enumerate(poly):
        if idx ==0:
            r = c
        else:
            r = r + (c *( x**idx))
    return r % mod

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
               o += int(m1[t]) * int(m2[t][c])
            row.append((o % mod))
    return row


#polynomial creation for shamir secret sharing  : deg = degree of polynomial, constant = the secret value , bound = max value for coefficients
#the poly returned is of the form [constant, x^3, x^2, x ] for a deg=3 polynomial . all values are coefficients
def createShamirPoly( deg,  constant,  bound):
    #print " in create poly, passed:  deg "  + str(deg) + " constant " + str(constant) + "  bound " + str(bound)
    if int(deg)<0:
        print("{0}[-] ERROR: Degree of polynomial requested < 0{1}".format(COLORS['FAIL'], COLORS['ENDC']))
        sys.exit(1)
    output = [constant]
    for x in xrange(0, deg-1):
        output.append(randint(1, bound-1))
    return output


#does lagrange interpolation for set of points, but is tweaked to quickly only compute the intercept value of the polynomial
#used only for shamir secret reformulation
def fastLagrangeInter_interceptOnly(points, n_mod):
    num_points = len(points)
    f = 0
    for idx, point in enumerate(points):
        L = 1
        for idx2 in xrange(num_points):
            if (idx2 !=idx):
                L *= (-points[idx2][0]/(point[0] -points[idx2][0]))
        f += (L * point[1])

    if f < 0:
        return n_mod + (f % n_mod)
    else:
        return f % n_mod
