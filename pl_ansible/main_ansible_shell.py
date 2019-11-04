#! /usr/bin/env python
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
import sys
import os
from subprocess import Popen, PIPE, STDOUT, call
BASE_DIR = os.path.abspath('.')
sys.path.append(BASE_DIR)

import re

def parseOption(argv):
    parser = ArgumentParser(description="version 1.0.0")
    parser.add_argument("-e", "--environment", dest="env", help="input the environment in which the script needs to be executed ",
                        metavar="[prod|stg|dev|...]")
    parser.add_argument("-g", "--group", dest="group", help="input the ansible hosts group",
                        metavar="[gp01|ip|...]")
    parser.add_argument("-c", "--command", dest="cmd", help="input the command",
                        metavar="[ls|cd|...]")
   
    args = parser.parse_args()
    if not len(argv): parser.print_help();sys.exit(1) 
    return args 

def ansible_cmd_func(hosts,forks,cmd):
    ansible_cmd = "ansible %s -f %s  -m shell -a '%s' " % (hosts,forks,cmd)
    try:        
        pcmd = Popen(ansible_cmd, stdout=PIPE, stderr=STDOUT, shell=True) 
        while True: 
            line = pcmd.stdout.readline().strip() 
            if line:
                print(line)
            else:
                break   
        
    except:
        exinfo=sys.exc_info()
        print (exinfo)
    
    retcode = pcmd.wait()
    if retcode == 0:
        pass
    else:
        raise Exception("Command failed")
def main(argv):
    options = parseOption(argv)
    hosts = options.group
    forks = 5
    cmd = options.cmd
    ansible_cmd_func(hosts,forks,cmd)
 
    

if __name__ == "__main__":
  
    main(sys.argv[1:])
    
