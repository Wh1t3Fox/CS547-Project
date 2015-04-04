#!/usr/bin/env python2
# Client scrript
# PIR - Goldbergs Protocol
#CS 54701 Project- Craig West & Michael Kouremetis


#Goldbergs Protocol
#Client creates shamir shares, crpto primatives, etc...  given parameters passed
#sends to shares to data bases with query emedded
# gets responses from databases and constructs query response


from Crypto.Util.number import getPrime
from ConfigParser import SafeConfigParser
from random import randint, choice
from Util import *
import sys
import os
import socket
import time
import csv
import argparse
import pickle


queries = [ ]      # list of query indexes
datab_hosts = [ ]  #list of database hosts to use
datab_ports = [ ]  #list of database port to use; ideally these would all be the same port but we are doing all local host testing so they are not

#functions
def query( hostname,  port,  data_to_send,  n_mod):
    serv_addr = hostname,  int(port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(serv_addr)
    data_to_send.append(n_mod)  #we need to send the server the modulus too, so attaching it as a last item on the list of pi's
    try:
        pickle_data = pickle.dumps(data_to_send)
        print " Sending Database:",  data_to_send
        s.sendall(pickle_data)
        data =pickle.loads( s.recv(100))
        #print data     # data should be a vector of length s (# of words per record/block) 
        return data
      
    except:
        print "[-] ERROR: tried to send/recieve a query request to database: {0}".format(serv_addr)


argsparser = argparse.ArgumentParser()
argsparser.add_argument("-l", "--servers", type=int, dest='l_num_datab', default=2, help="the # of databases for the system")
argsparser.add_argument("-t", "--collude", type=int, dest='t_priv_num_datab', default=2, help="the # of databases that can collude and still not obtain query, t+1 servers must collude to break IT-PIR")
argsparser.add_argument("-r", "--respond", type=int, dest='k_req_num_datab', default=0, help="the # of databases that need to respond to query and query still be successfully retrieved")
argsparser.add_argument("-m", "--malicious", type=int, dest='v_byz_num_datab', default=0, help="the # of databases ( v of k ) that can be malicious, i.e. lie or be erroneous for query to still be successful")
argsparser.add_argument("-q", "--query", dest='query_set_fn', default='PIR-Queries.csv', help="filename of set of queries to make the servers; format of file is probably just indexes  by csv , 10 per row")
argsparser.add_argument("-d", "--database", dest='datab_config', default='PIR-Databases.csv', help="filename of set of databases addresses to use; format is (host, port, db type) , one per line")
argsparser.add_argument("-v", "--verbose", action="store_true", help="test output")
args = argsparser.parse_args()

parser = SafeConfigParser()
parser.read('config.ini')

#more parameters

db_tsize_bits = int(parser.get('params', 'db_tsize_bits'))
block_size_bits = int(parser.get('params', 'block_size_bits'))   #aka record size
word_size_bits = int(parser.get('params', 'word_size_bits'))
r_numRecords = db_tsize_bits/block_size_bits
s_words_per_block = block_size_bits/word_size_bits

#integer field parameters for Shamir Polynomials
p = getPrime(word_size_bits)
q = getPrime(word_size_bits)
n_mod = p*q
shamir_indices_I = [ ]


print " Databases: " + str(args.l_num_datab) + "  Records: " + str(r_numRecords)  + " Database Config File: " + str(args.datab_config) + " Queries Config File: " + str(args.query_set_fn) + " Interger Ring: " + str(n_mod)  + " p:" + str(p) + " q:" + str(q)

print "\n-------------- PIR-Goldberg Client------------\n"


#getting set II which is a set of proper indices ( x input values) to use with the poly functions on Shamir
#for x in xrange(0, 8*args.l_num_datab):    #8 is just a random factor, to make the total indice size to draw from 8x as big as needed
#   temp = randint(1, min(p, q)-1)
#    shamir_indices_I.append(temp)
    
for x in xrange(args.l_num_datab):
    shamir_indices_I.append(x +1)
########TODO shamir indices above need to be 1,2,3,4,5 etc... the interpolation doesnt work well with random x inputs

# read in qeuries to make to databases
try:
    with open(args.query_set_fn ,"r") as csvfile:
        d = csv.reader(csvfile, delimiter = ',')
        for row in d:
            for i in range(0, len(row)):
                queries.append(row[i])
except IOError:
    print "[-] IO error on {0}".format(args.query_set_fn)

print "------Have list of queries to make"
print "      " + str(queries)
# read in databases addresses
#technically this config file does have the information on which databases are malicious/good but this information
# is not used/read in to the client
try:
    with open(args.datab_config ,"r") as csvfile:
        d = csv.reader(csvfile, delimiter = ',')
        for row in d:
            datab_hosts.append(row[0])
            datab_ports.append(row[1])
except IOError:
    print "[-] IO error on {0}".format(args.datab_config)

print "------Have list of databases"
print "       " + str(datab_hosts)

#check 
if(len(datab_hosts) != args.l_num_datab):
    print "ERROR: number of databases read in from config file does not match the number of databases told to the client via parameters"




#Conduct queries
print "------Queries: "
for idx, q in enumerate(queries):
    print " conducting query , query index(record wanted): "  + str(q) + "\n"
   # Choose L random distinct indices alpha-1...alpha-l from set II
    #L_indices = list(set( ))
    #while len(L_indices) < args.l_num_datab:
    #   L_indices.append(choice(shamir_indices_I))
    L_indices = shamir_indices_I

    print "     Created L indices (x inputs)"
    print "       " + str(L_indices) 
    #choose/create r random polynomials f-1 ... f-r of degree t. The coefficients are random, the constant terms are 0's except for 1 where r = q (query number)
    r_polyFunc = [ ]
    for x in xrange(r_numRecords):
        if x == int(q):
            r_polyFunc.append(createShamirPoly( args.t_priv_num_datab, 1,n_mod ) )
        else:
            r_polyFunc.append(createShamirPoly( args.t_priv_num_datab, 0, n_mod ) )

    print "      Created r(num of records) shamir polynomials "
    print "       " +  str(r_polyFunc)
    #get p-i 's ( output y) using each corresponding value in L_indices and r_polyFunc. Each server will outputs from every poly function
    pi_server_vectors = [ ]
    for c in xrange(args.l_num_datab):
        p = [ ]
        for f in xrange( r_numRecords):
            p.append(polyEval(r_polyFunc[f],L_indices[c] , n_mod))
        pi_server_vectors.append(p)

    print "      Created p_i s(vectors of y outputs ) "
    print "       " + str(pi_server_vectors)
    
    
    
    #make database connections
    #conduct communication
    Rs = [ ]
    for idx2, x in enumerate(datab_hosts):
        print "     querying database: {0} {1} for query {2}: Record {3}".format(datab_hosts[idx2], datab_ports[idx2], idx, q)
        time.sleep(3)
        R = query(datab_hosts[idx2],  datab_ports[idx2],  pi_server_vectors[idx2], n_mod)  
        Rs.append(R)
    print "      Rij s Received:\n" + str(Rs)
    
    #decode response
    record = [] 
    for c in xrange(s_words_per_block):
        pts = [] 
        for idx, x in enumerate(L_indices):
            tmp = [x, Rs[idx][c]]   
            pts.append(tmp)
        print "     Points made: "
        print str(pts)
        intercept = fastLagrangeInter_interceptOnly(pts)
        if(intercept< 0):
            record.append(n_mod + (intercept % n_mod))
        else:
            record.append(intercept % n_mod )
    print " Record Retrieved: " + str(record)
    print" --------------------------------------------------------------"
    
    
    
    
    
    
    
