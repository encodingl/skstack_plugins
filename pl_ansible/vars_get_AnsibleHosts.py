#! /usr/bin/env python
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
import sys
import os
import json
BASE_DIR = os.path.abspath('.')
sys.path.append(BASE_DIR)

import re

def parseOption(argv):
    parser = ArgumentParser(description="version 1.0.0")
    parser.add_argument("-e", "--environment", dest="env", help="input the environment in which the script needs to be executed ",
                        metavar="[prod|stg|...]")
   
    args = parser.parse_args()
    if not len(argv): parser.print_help();sys.exit(1)
    return args 

def get_AnsibleHostsDic(args):
    dic = {}
    pattern = r'^\s*\[.+\]'

    with open(args) as f:
        for line in f:
            temp = line.split()
            if temp:
                m = re.search(pattern,line)

                if (m is not None):
                    g = m.group().strip().strip('[').strip(']')
                    dic[g] = []
                else:
                    try:
                        dic[g].append(line)
                    except:
                        pass
                    
  
    list_group_key = list(dic.keys())
    list_group_key.sort()

    return list_group_key
def main(argv):
    options = parseOption(argv)
    config_file = options.env+"_conf.json"
   
    CONFIGFILE = os.path.join(BASE_DIR, 'conf', config_file)
    
    
    if os.path.exists(CONFIGFILE):
        
        with open(CONFIGFILE, "r") as f:
            line = f.readline()
            d=json.loads(line)
            ansible_hosts_file = d["ansible_hosts_file"]
            print(ansible_hosts_file)
        
    else:
        print("%s is not exist" % CONFIGFILE)
        sys.exit(1)
    
    
 
    
    list_group_key=get_AnsibleHostsDic(ansible_hosts_file)
    print(list_group_key)
    

if __name__ == "__main__":
    main(sys.argv[1:])
    
