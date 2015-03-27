#!/usr/bin/env python2
# PIR Database script - this script takes parameters to become a type of database to be used
# PIR - Goldbergs Protocol
# CS 54701 Project- Craig West & Michael Kouremetis

import sys
import threading
import socket
import time
import csv
import argparse

dbs = [ ]     #this holds all the information from the database config file; this database instance will use its
              #specified index to get the parameters for its own database


#client thread handler
def client_handler(client):
    d = client.recv(16)
    print "received from client:", d
    s = "server request confirmation"
    client.sendall(s)
    client.close()

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--index", type=int, dest='index', help="the row index of the database config file that corresponds to this database")
parser.add_argument("-d", "--database", dest='datab_config', help="filename of set of databases addresses to use; format is (host, port, db type, db content) , one per line")
args = parser.parse_args()

#read in database info of all databases
try:
    with open(args.datab_config ,"r") as csvfile:
        d = csv.reader(csvfile, delimiter = ',')
        for row in d:
            # row[0] = host , row[1] = port , row[2] = db type , row[3] = database content
            tmp = [row[0],  row[1],  row[2],  row[3]]
            dbs.append(tmp)
except IOError:
    print" IO error on ", args.datab_config
    time.sleep(3)

#get database config info for this database
server_addr = dbs[args.index][0] , int(dbs[args.index][1])   #host , port
db_type = dbs[args.index][2] # types : 0 = normal database   1= dont respond 2 =  erroneous 3 = malicious
db_cont = dbs[args.index][3]

#read in database content for this database
#start database
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_addr)
sock.listen(5)
print " -- Database Server -- Type {0}".format(db_type)
print " Ready -  server address : {0}".format(server_addr)
time.sleep(3)
while True:
    try:
        client, client_addr = sock.accept()
        print 'connection from {0}'.format(client_addr)
        t = threading.Thread(target = client_handler,  args = [client])
        t.start()     #pop a thread off to handle request

    except:
        client.close()
        break
