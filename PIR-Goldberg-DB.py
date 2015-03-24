#!/usr/bin/env python
# PIR Database script - this script takes parameters to become a type of database to be used
# PIR - Goldbergs Protocol
#CS 54701 Project- Craig West & Michael Kouremetis

import sys
import threading
import socket
import time
import csv

#client thread handler
def client_handler(client):
    d = client.recv(16)
    print "received from client:", d
    s = "server request confirmation"
    client.sendall(s)
    client.close()
    

#get command arguments
index = int(sys.argv[1] )             #the row index of the database config file that corresponds to this database  
datab_config = sys.argv[2]         #filename of set of databases addresses to use; format is (host, port, db type, db content) , one per line

#database variables
dbs = [ ]                                      #this holds all the information from the database config file; this database instance will use its 
                                                    #specified index to get the parameters for its own database
 
#read in database info of all databases -----------------------------------------------------------------------------------------------
try:
    with open(datab_config ,"r") as csvfile:
        d = csv.reader(csvfile, delimiter = ',')
        for row in d:
            tmp = [row[0],  row[1],  row[2],  row[3]]    # row[0] = host , row[1] = port , row[2] = db type , row[3] = database content
            dbs.append(tmp)
except IOError:
    print" IO error on ", datab_config
    time.sleep(3)

#get database config info for this database --------------------------------------------------------------------------------------------
server_addr = dbs[index][0] , int(dbs[index][1])   #host , port
type = dbs[index][2]                                             # types : 0 = normal database   1= dont respond 2 =  erroneous 3 = malicious
db_cont = dbs[index][3]

#read in database content for this database ----------------------------------------------------------------------------------------------



#start database ------------------------------------------------------------------------------------------------------------------------------------------
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_addr)
sock.listen(5)
print " -- Database Server -- Type ",  type
print " Ready -  server address : ", server_addr
time.sleep(3)
while True:
    try:
        client, client_addr = sock.accept()
        print 'connection from', client_addr
        t = threading.Thread(target = client_handler,  args = [client])
        t.start()     #pop a thread off to handle request
            
    except:
        client.close()
        break

