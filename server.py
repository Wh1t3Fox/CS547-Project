#!/usr/bin/env python2
# PIR Database script - this script takes parameters to become a type of database to be used
# PIR - Goldbergs Protocol
# CS 54701 Project- Craig West & Michael Kouremetis

from ConfigParser import SafeConfigParser
from Util import *
import sys
import threading
import socket
import time
import csv
import argparse
import pickle

dbs = [ ]     #this holds all the information from the database config file; this database instance will use its
              #specified index to get the parameters for its own database

#client thread handler
def client_handler(client,  db_cont):
    d = client.recv(r_numRecords * block_size_bits)
    print "received from client:" + str(len(d))  +  "bits"
    p_i = pickle.loads(d)
    print "pi vector from client: " + str( p_i)
    s = pickle.dumps(matrixMult(p_i, db_cont))
    client.sendall(s)
    client.close()

argsparser = argparse.ArgumentParser()
argsparser.add_argument("-i", "--index", type=int, dest='index', required = True,  help="the row index of the database config file that corresponds to this database")
argsparser.add_argument("-d", "--database", dest='datab_config', required = True,  help="filename of set of databases addresses to use; format is (host, port, db type, db content) , one per line")
args = argsparser.parse_args()

parser = SafeConfigParser()
parser.read('config.ini')

#more parameters
db_tsize_bits = parser.get('params', 'db_tsize_bits')
block_size_bits = parser.get('params', 'block_size_bits')   #aka record size
word_size_bits = parser.get('params', 'word_size_bits')
r_numRecords = db_tsize_bits/block_size_bits
s_words_per_block = block_size_bits/word_size_bits

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
db_cont_fn = dbs[args.index][3]


#read in database content for this database
db_cont = [ ]   #list  of rows of the db, a row is a record. For now , 1 record is 4 - 8 bit numbers
try:
    with open(db_cont_fn ,"r") as csvfile:
        d = csv.reader(csvfile, delimiter = ',')
        for row in d:
            tmp = [row[0],  row[1],  row[2],  row[3]]
            db_cont.append(tmp)
except IOError:
    print" IO error on ", db_cont_fn
    time.sleep(3)


#start database
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_addr)
sock.listen(5)
print "--------- Database Server -- Type {0}--------------".format(db_type)
print " Ready -  server address : {0}".format(server_addr)
time.sleep(3)
while True:
    try:
        client, client_addr = sock.accept()
        print 'connection from {0}'.format(client_addr)
        t = threading.Thread(target = client_handler,  args = [client, db_cont])
        t.start()     #pop a thread off to handle request

    except:
        client.close()
        break
