#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Part1:Load dependent library
from argparse import ArgumentParser
import sys
import os
import re

# Part2:load skstack_plugins env to sys
CONFIG_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Part3:load skstack lib_pub module 
from lib_pub.common import load_pri_json_conf

# Part4:Define optional variables
def parseOption(argv):
    parser = ArgumentParser(description="version 1.0.0")
    parser.add_argument("-e", "--environment", dest="env", help="input the environment in which the script needs to be executed ",
                        metavar="[prod|stg|...]")
   
    args = parser.parse_args()
    if not len(argv): parser.print_help();sys.exit(1)
    return args 

# Part5:Define the task function
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

# Part6:Define the main function,accept parameters passed to the task function to executes 
def main(argv):
    options = parseOption(argv)
    env = options.env
    ansible_hosts_file = load_pri_json_conf(CONFIG_BASE_DIR,env, "ansible_hosts_file")

    list_group_key=get_AnsibleHostsDic(ansible_hosts_file)
    print(list_group_key)
    

if __name__ == "__main__":
    main(sys.argv[1:])
    
