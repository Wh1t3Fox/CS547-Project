#!/usr/bin/env python
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
        print "Error: tried to send/recieve a query request to database:" ,  serv_addr


#get command arguments
l_num_datab = int(sys.argv[1])             #the number of databases for the system
t_priv_num_datab = int(sys.argv[2])     #the number of databases that can collude and still not obtain query, t+1 servers must collude to break IT-PIR
k_req_num_datab = int(sys.argv[3])     # the number of databases that need to respond to query and query still be successfully retrieved
v_byz_num_datab = int(sys.argv[4])      # the number of databases ( v of k ) that can be malicious, i.e. lie or be erroneous for query to still be successful
query_set_fn = sys.argv [5]            #filename of set of queries to make the servers; format of file is probably just indexes  by csv , 10 per row
datab_config = sys.argv[6]             #filename of set of databases addresses to use; format is (host, port) , one per line
verbose = False                                #test output on = True , off = False

queries = [ ]          # list of query indexes
datab_hosts = [ ]  #list of database hosts to use
datab_ports = [ ]  #list of database port to use; ideally these would all be the same port but we are doing all local host testing so they are not

print " -- PIR-Goldberg Client --"
# read in qeuries to make to databases---------------------------------------------------------------------------------------------------------------------------
try:
    with open(query_set_fn ,"r") as csvfile:
        d = csv.reader(csvfile, delimiter = ',')
        for row in d:
            for i in range(0, len(row)):
                queries.append(row[i])
except IOError:
    print" IO error on ", query_set_fn

print"Have list of queries to make..."

# read in databases addresses---------------------------------------------------------------------------------------------------------------------------
#technically this config file does have the information on which databases are malicious/good but this information
# is not used/read in to the client
try:
    with open(datab_config ,"r") as csvfile:
        d = csv.reader(csvfile, delimiter = ',')
        for row in d:
            datab_hosts.append(row[0])
            datab_ports.append(row[1])
except IOError:
    print" IO error on ", datab_config
    
    
print "Have list of databases..."
    
#Conduct queries----------------------------------------------------------------------------------------------------------------------------------------------------------------
for idx, q in enumerate(queries):
    print " conducting query"
   # set up parameters of protocol
    #make database connections
    #conduct communication
    for idx2, x in enumerate(datab_hosts):
        print "querying database:" ,  datab_hosts[idx2], " ",  datab_ports[idx2],  "for query ",  idx ,  ": ",  q
        time.sleep(3)
        response = query(datab_hosts[idx2],  datab_ports[idx2],  q)
    #decode response
    
