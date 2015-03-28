#!/usr/bin/env python2
# Client scrript
# PIR - Goldbergs Protocol
#CS 54701 Project- Craig West & Michael Kouremetis


#Goldbergs Protocol
#Client creates shamir shares, crpto primatives, etc...  given parameters passed
#sends to shares to data bases with query emedded
# gets responses from databases and constructs query response

import sys
import os
import socket
import time
import csv
import argparse
from Util import *
from Cyrpto.Util.number import getPrime
from random import randint,  choice
import pickle


queries = [ ]      # list of query indexes
datab_hosts = [ ]  #list of database hosts to use
datab_ports = [ ]  #list of database port to use; ideally these would all be the same port but we are doing all local host testing so they are not

#functions
def query( hostname,  port,  data_to_send):
    serv_addr = hostname,  int(port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(serv_addr)
    try:
        data_to_send = pickle.dumps(pi_server_vectors)
        s.sendall(data_to_send)
        data = s.recv(32)
        print data
        #recieve data, not sure of format yet
    except:
        print "[-] ERROR: tried to send/recieve a query request to database: {0}".format(serv_addr)


parser = argparse.ArgumentParser()
parser.add_argument("-l", "--servers", type=int, dest='l_num_datab', help="the # of databases for the system")
parser.add_argument("-t", "--collude", type=int, dest='t_priv_num_datab', help="the # of databases that can collude and still not obtain query, t+1 servers must collude to break IT-PIR")
parser.add_argument("-r", "--respond", type=int, dest='k_req_num_datab', help="the # of databases that need to respond to query and query still be successfully retrieved")
parser.add_argument("-m", "--malicious", type=int, dest='v_byz_num_datab', help="the # of databases ( v of k ) that can be malicious, i.e. lie or be erroneous for query to still be successful")
parser.add_argument("-q", "--query", dest='query_set_fn', help="filename of set of queries to make the servers; format of file is probably just indexes  by csv , 10 per row")
parser.add_argument("-d", "--database", dest='datab_config', help="filename of set of databases addresses to use; format is (host, port, db type) , one per line")
parser.add_argument("-v", "--verbose", action="store_true", help="test output")
args = parser.parse_args()

print " -- PIR-Goldberg Client --"

#more parameters
db_tsize_bits = 320
block_size_bits = 32   #aka record size
word_size_bits = 8
r_numRecords = db_tsize_bits/block_size_bits
s_words_per_block = block_size_bits/word_size_bits

#integer field parameters for Shamir Polynomials
p = getPrime(2**word_size_bits)
q = getPrime(2**word_size_bits)
n_mod = p*q
shamir_indices_I = [ ]

#getting set II which is a set of proper indices ( x input values) to use with the poly functions on Shamir
for x in xrange(0, 8*l_num_datab):    #8 is just a random factor, to make the total indice size to draw from 8x as big as needed
    temp = randint(1, min(p, q)-1)
    shamir_indices_I.append(temp)

# read in qeuries to make to databases
try:
    with open(args.query_set_fn ,"r") as csvfile:
        d = csv.reader(csvfile, delimiter = ',')
        for row in d:
            for i in range(0, len(row)):
                queries.append(row[i])
except IOError:
    print "[-] IO error on {0}".format(args.query_set_fn)

print "Have list of queries to make..."

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

print "Have list of databases..."

#Conduct queries
for idx, q in enumerate(queries):
    print " conducting query"
   # Choose L random distinct indices alpha-1...alpha-l from set II
    L_indices = set( )
    while L_indices < l_num_datab:
        L_indices.add(choice(shamir_indices_I))

    print " created L indices (x inputs)"

    #choose/create r random polynomials f-1 ... f-r of degree t. The coefficients are random, the constant terms are 0's except for 1 where r = q (query number)
    r_polyFunc = [ ]
    for x in xrange(r_numRecords):
        if(x ==q):
            r_polyFunc.append(createShamirPoly( t_priv_num_datab, 1,n_mod ) )
        else:
            r_polyFunc.append(createShamirPoly( t_priv_num_datab, 0, n_mod ) )

    print " created r(num of records) shamir polynomials "

    #get p-i 's ( output y) using each corresponding value in L_indices and r_poly_func. Each server will outputs from every poly function
    pi_server_vectors = [ ]
    for c in xrange(l_num_datab):
        p = [ ]
        for f in xrange( r_numRecords):
            p.append(polyEval(r_poly_func[f],L_indices[c] ))
        pi_server_vectors.append(p)

    print " created p_i's(vectors of y outputs with each 1 indice and all poly functions)  "

    #make database connections
    #conduct communication
    for idx2, x in enumerate(datab_hosts):
        print " querying database: {0} {1} for query {2}: {3}".format(datab_hosts[idx2], datab_ports[idx2], idx, q)
        time.sleep(3)
        response = query(datab_hosts[idx2],  datab_ports[idx2],  q)
    #decode response
