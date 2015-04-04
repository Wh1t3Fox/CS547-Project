#Test Run through of Goldberg protocol
# the database, shamir polynomials and parameters are all hard coded


#evaluate a given polynomial and x, to return the output y
def polyEval( poly ,  x,  mod):
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
   # print " m1_c = " + str(m1_c) + " m2_r = " + str(m2_r) + " m2_c = " + str(m2_c)
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

#TODO , changed both of these functions above from original ..Notably Matrix Mult did too many calculations so fixed it

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
    
p = [[1.0, 341.0],  [2.0, 11.0],  [3.0, 171.0], [4, 402]]

print fastLagrangeInter_interceptOnly(p)

#---------------------------------------------------------------------------#
L =4  #num databases
t=3   #num servers
n= 128 #bits in database
b = 32 #block size in bits
w =8 #word size in bits

r= n/b  #num of records  
s= b/w #words per block


p= 251  #random  prime p
q= 69  #random prime q
S = p *q   #integer ring    527
print " S is " + str(S)

db = [[1, 4, 4, 1], [1, 2, 2, 1] , [1, 16, 16, 10], [526, 13, 1, 8]]

#--------------------------------------------------------------------------#
#Client
alphas = [1.0,  2.0,  3.0,  4.0]  #x instances

#random polynomials, constant of f_3 is  1 bc block wanted is 3
#need 4 polynomials because 4 overall records in database
f_1= [0, 10, 45, 8]
f_2 = [0,  27,  87,  6]
f_3 = [0,  222,  61,  7]
f_4= [1, 72, 56, 3]
pf = [ ]
pf.append(f_1)
pf.append(f_2)
pf.append(f_3)
pf.append(f_4)

#p_i 's to giver to servers
p_i = [ ]
for idx,x in enumerate(alphas):
    tmp = []
    for idx2, y in enumerate(pf):
        tmp.append(polyEval(y, x,  S)) 
    print " p_i: " + str(idx) + " " + str(tmp)
    p_i.append(tmp)
    
        
        
#-------------------------------------------------------------------------#
#Servers
R =[]
for idx, p in enumerate(p_i):
    m = matrixMult(p , db, S)
    print " Server: " + str(idx) + " returns " + str(m)
    R. append(m)

 #---------------------------------------------------------------#
 #Client

 #make points for lagrange interpolation for every word
li = []
for idx in xrange(s):
    d = []
    print "points for word: " + str(idx +1)
    for idx2 in xrange(L):
        f= [alphas[idx2], R[idx2][ idx]]
        d.append(f)
    print d
    intercept = fastLagrangeInter_interceptOnly(d)
    print " intercept is " + str(intercept)
    print " decoded word: " + str( intercept % S)
   

#from here i just entered the points into wolfram alpha's langrange interpolation calculator to get the polynomial, then mod constant term


# So this is strange:

#When the lagrange itnerpolation function is created from the points, two things can happen:
# 1. If the constant term (x) is positive, no problem, just do x mod S , and theres word i of the record
#2. But if the constant term(x) is negative, you have to do S - |x mod S|   OR   S + (x mod S) to get word i of the record.
