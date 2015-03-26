#!/usr/bin/env python2
# Creation script - this creates a client process and a set of server databases (all locally) that will conduct Goldbergs PIR protocol
# PIR - Goldbergs Protocol
# CS 54701 Project- Craig West & Michael Kouremetis

from subprocess import Popen
import sys
import time
import argparse


parser = argparse.ArgumentParser(description='Launch the Client and DB for PIR')
parser.add_argument("-n", "--n", type=int, dest='l_num_datab', nargs='?', default=2, help="the # of databases for the system")
parser.add_argument("-c", "--collude", type=int, dest='t_priv_num_datab', nargs='?', default=0, help="the # of databases that can collude and still not obtain query, t+1 servers must collude to break IT-PIR")
parser.add_argument("-r", "--respond", type=int, dest='k_req_num_datab', nargs='?', default=0, help="the # of databases that need to respond to query and query still be successfully retrieved")
parser.add_argument("-m", "--malicious", type=int, dest='v_byz_num_datab', nargs='?', default=0, help="the # of databases ( v of k ) that can be malicious, i.e. lie or be erroneous for query to still be successful")
parser.add_argument("-q", "--query", dest='query_set_fn', nargs='?', default='PIR-Queries.csv', help="filename of set of queries to make the servers; format of file is probably just indexes  by csv , 10 per row")
parser.add_argument("-d", "--database", dest='datab_config', nargs='?', default='PIR-Databases.csv', help="filename of set of databases addresses to use; format is (host, port, db type) , one per line")
args = parser.parse_args()


# Set up databases (servers) first
#this opens up a terminal for every server started so can observe it
for index in xrange(0, args.l_num_datab):
    time.sleep(1)
    Popen('''gnome-terminal -e 'bash -c "python PIR-Goldberg-DB.py {0} {1}"' '''.format(index, args.datab_config), shell=True)

time.sleep(3)

#Set up client
Popen('''gnome-terminal -e 'bash -c "python client.py -n {0} -c {1} -r {2} -m {3} -q {4} -d {5}"'  '''.format(args.l_num_datab, args.t_priv_num_datab,
    args.k_req_num_datab, args.v_byz_num_datab, args.query_set_fn, args.datab_config), shell=True)
