#!/usr/bin/env python
# Creation script - this creates a client process and a set of server databases (all locally) that will conduct Goldbergs PIR protocol
# PIR - Goldbergs Protocol
#CS 54701 Project- Craig West & Michael Kouremetis

import os
import sys
import time


l_num_datab = 2                                   #the # of databases for the system
t_priv_num_datab = 0                              #the # of databases that can collude and still not obtain query, t+1 servers must collude to break IT-PIR
k_req_num_datab = 0                             # the # of databases that need to respond to query and query still be successfully retrieved
v_byz_num_datab = 0                               # the # of databases ( v of k ) that can be malicious, i.e. lie or be erroneous for query to still be successful
query_set_fn = "PIR-Queries.csv"          #filename of set of queries to make the servers; format of file is probably just indexes  by csv , 10 per row
datab_config = "PIR-Databases.csv"      #filename of set of databases addresses to use; format is (host, port, db type) , one per line

#TODO: make the above argument parameters 

# Set up databases (servers) first --------------------------------------------------------------------------------------------
#this opens up a terminal for every server started so can observe it
for index in range(0, l_num_datab):
    c = "gnome-terminal -e 'bash -c \" python PIR-Goldberg-DB.py " + str(index) +" " + datab_config + " \"'"
    os.system(c)
    
time.sleep(3)
#Set up client ---------------------------------------------------------------------------------------------------------------------------
c = "gnome-terminal -e 'bash -c \" python PIR-Goldberg-Client.py " + str(l_num_datab) +" " + str(t_priv_num_datab) + " " + str(k_req_num_datab) + \
" " + str(v_byz_num_datab) + " " + " "  + query_set_fn + " " +  datab_config + " \"'"
os.system(c)
