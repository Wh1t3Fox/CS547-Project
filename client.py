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


queries = [ ]      # list of query indexes
datab_hosts = [ ]  #list of database hosts to use
datab_ports = [ ]  #list of database port to use; ideally these would all be the same port but we are doing all local host testing so they are not

#functions
def query( hostname,  port,  data_to_send):
    serv_addr = hostname,  int(port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(serv_addr)
    try:
        s.sendall(data_to_send)
        data = s.recv(32)
        print data
        #recieve data, not sure of format yet
    except:
        print "[-] ERROR: tried to send/recieve a query request to database: {0}".format(serv_addr)


parser = argparse.ArgumentParser()
parser.add_argument("-n", "--n", type=int, dest='l_num_datab', help="the # of databases for the system")
parser.add_argument("-c", "--collude", type=int, dest='t_priv_num_datab', help="the # of databases that can collude and still not obtain query, t+1 servers must collude to break IT-PIR")
parser.add_argument("-r", "--respond", type=int, dest='k_req_num_datab', help="the # of databases that need to respond to query and query still be successfully retrieved")
parser.add_argument("-m", "--malicious", type=int, dest='v_byz_num_datab', help="the # of databases ( v of k ) that can be malicious, i.e. lie or be erroneous for query to still be successful")
parser.add_argument("-q", "--query", dest='query_set_fn', help="filename of set of queries to make the servers; format of file is probably just indexes  by csv , 10 per row")
parser.add_argument("-d", "--database", dest='datab_config', help="filename of set of databases addresses to use; format is (host, port, db type) , one per line")
parser.add_argument("-v", "--verbose", action="store_true", help="test output")
args = parser.parse_args()

print " -- PIR-Goldberg Client --"
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
   # set up parameters of protocol
    #make database connections
    #conduct communication
    for idx2, x in enumerate(datab_hosts):
        print " querying database: {0} {1} for query {2}: {3}".format(datab_hosts[idx2], datab_ports[idx2], idx, q)
        time.sleep(3)
        response = query(datab_hosts[idx2],  datab_ports[idx2],  q)
    #decode response
