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
from lagrange import *
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
        print "{0}[+] Sending Database:{1}{2} {3}{4}\n".format(COLORS['OKGREEN'], COLORS['ENDC'], COLORS['OKBLUE'], data_to_send, COLORS['ENDC'])
        s.sendall(pickle_data)
        data =pickle.loads( s.recv(100))
        #print data     # data should be a vector of length s (# of words per record/block)
        return data

    except:
        print "{0}[-] ERROR: tried to send/recieve a query request to database: {1}{2}".format(COLORS['FAIL'], serv_addr, COLORS['ENDC'])


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
shamir_indices_I = []

print "\n{0}-------------- PIR-Goldberg Client------------{1}\n".format(COLORS['HEADER'], COLORS['ENDC'])

print "{0}[+] Databases:{1}{2} {3}{4}".format(COLORS['OKGREEN'], COLORS['ENDC'], COLORS['OKBLUE'], str(args.l_num_datab), COLORS['ENDC'])
print "{0}[+] Records:{1}{2} {3}{4}".format(COLORS['OKGREEN'], COLORS['ENDC'], COLORS['OKBLUE'], str(r_numRecords), COLORS['ENDC'])
print "{0}[+] Database Config File:{1}{2} {3}{4}".format(COLORS['OKGREEN'], COLORS['ENDC'], COLORS['OKBLUE'], str(args.datab_config), COLORS['ENDC'])
print "{0}[+] Queries Config File:{1}{2} {3}{4}".format(COLORS['OKGREEN'], COLORS['ENDC'], COLORS['OKBLUE'], str(args.query_set_fn), COLORS['ENDC'])
print "{0}[+] Interger Ring:{1}{2} {3} p: {4} q: {5}".format(COLORS['OKGREEN'], COLORS['ENDC'], COLORS['OKBLUE'], str(n_mod), str(p), str(q), COLORS['ENDC'])


#getting set II which is a set of proper indices ( x input values) to use with the poly functions on Shamir
#for x in xrange(0, args.l_num_datab):    #8 is just a random factor, to make the total indice size to draw from 8x as big as needed
#   temp = randint(1, min(p, q)-1)
#   shamir_indices_I.append(temp)

for x in xrange(args.l_num_datab):
    shamir_indices_I.append(x +1)


# read in qeuries to make to databases
try:
    with open(args.query_set_fn ,"r") as csvfile:
        d = csv.reader(csvfile, delimiter = ',')
        for row in d:
            for i in range(0, len(row)):
                queries.append(row[i])
except IOError:
    print "{0}[-] IO error on {1}{2}".format(COLORS['FAIL'],args.query_set_fn, COLORS['ENDC'])

print "{0}[+] Have list of queries to make:{1}{2} {3}{4}\n ".format(COLORS['OKGREEN'], COLORS['ENDC'], COLORS['OKBLUE'], str(queries), COLORS['ENDC'])

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
    print "{0}[-] IO error on {1}{2}".format(COLORS['FAIL'], args.datab_config, COLORS['ENDC'])

print "{0}[+] Have list of databases:{1}{2} {3}{4}\n".format(COLORS['OKGREEN'], COLORS['ENDC'], COLORS['OKBLUE'], str(datab_hosts), COLORS['ENDC'])

#check
if(len(datab_hosts) != args.l_num_datab):
    print "{0}[-] ERROR: number of databases read in from config file does not match the number of databases told to the client via parameters{1}".format(COLORS['FAIL'], COLORS['ENDC'])




#Conduct queries
for idx, q in enumerate(queries):
    print "{0}[+] Query index(record wanted):{1}{2} {3}{4}\n".format(COLORS['OKGREEN'], COLORS['ENDC'], COLORS['OKBLUE'], str(q), COLORS['ENDC'])

    L_indices = shamir_indices_I

    print "{0}[+] Created L indices (x inputs):{1}{2} {3}{4}\n".format(COLORS['OKGREEN'], COLORS['ENDC'], COLORS['OKBLUE'], str(L_indices), COLORS['ENDC'])
    #choose/create r random polynomials f-1 ... f-r of degree t. The coefficients are random, the constant terms are 0's except for 1 where r = q (query number)
    r_polyFunc = [ ]
    for x in xrange(r_numRecords):
        if x == int(q):
            r_polyFunc.append(createShamirPoly( args.t_priv_num_datab, 1,n_mod ) )
        else:
            r_polyFunc.append(createShamirPoly( args.t_priv_num_datab, 0, n_mod ) )

    print "{0}[+] Created r(num of records) shamir polynomials:{1}{2} \n{3}{4}\n".format(COLORS['OKGREEN'], COLORS['ENDC'], COLORS['OKBLUE'], '\n'.join(str(x) for x in r_polyFunc), COLORS['ENDC'])
    #get p-i 's ( output y) using each corresponding value in L_indices and r_polyFunc. Each server will outputs from every poly function
    pi_server_vectors = [ ]
    for c in L_indices:
        p = [ ]
        for f in r_polyFunc:
            p.append(polyEval(f, c, n_mod))
        pi_server_vectors.append(p)

    print "{0}[+] Created p_i s(vectors of y outputs ):{1}{2} \n{3}{4}\n".format(COLORS['OKGREEN'], COLORS['ENDC'], COLORS['OKBLUE'], '\n'.join(str(x) for x in pi_server_vectors), COLORS['ENDC'])



    #make database connections
    #conduct communication
    Rs = [ ]
    for idx2, x in enumerate(datab_hosts):
        print "{0}[+] Querying database:{1}{2} {3} {4} for query {5}: Record {6}{7}".format(
            COLORS['OKGREEN'], COLORS['ENDC'], COLORS['OKBLUE'], datab_hosts[idx2], datab_ports[idx2], idx, q, COLORS['ENDC'])
        time.sleep(3)
        R = query(datab_hosts[idx2],  datab_ports[idx2],  pi_server_vectors[idx2], n_mod)
        Rs.append(R)
    print "{0}[+] Rij s Received:{1}{2} {3}{4}\n".format(COLORS['OKGREEN'], COLORS['ENDC'], COLORS['OKBLUE'], ''.join(str(x) for x in Rs), COLORS['ENDC'])

    #decode response
    record = []
    for c in xrange(s_words_per_block):
        pts = []
        #make sure we only use idx for the number of DB we have
        for idx, x in enumerate(L_indices[0:len(datab_hosts)]):
            tmp = [x, Rs[idx][c]]
            pts.append(tmp)
        print "{0}[+] Points made:{1}{2} {3}{4}".format(COLORS['OKGREEN'], COLORS['ENDC'], COLORS['OKBLUE'], ''.join(str(x) for x in pts), COLORS['ENDC'])
        intercept = fastLagrangeInter_interceptOnly(pts, n_mod)
        record.append(intercept)
    print "{0}[+] Record Retrieved:{1}{2} {3}{4}".format(COLORS['OKGREEN'], COLORS['ENDC'], COLORS['OKBLUE'], str(record), COLORS['ENDC'])
    print"{0}--------------------------------------------------------------{1}".format(COLORS['HEADER'], COLORS['ENDC'])

#used to keep the terminal open
#until you want to close
raw_input("{0}[+] SUCCESS{1}".format(COLORS['OKGREEN'], COLORS['ENDC']))
