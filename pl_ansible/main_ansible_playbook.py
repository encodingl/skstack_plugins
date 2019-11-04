#! /usr/bin/env python
# -*- coding: utf-8 -*-
from optparse import OptionParser
import sys
import os
from subprocess import Popen, PIPE, STDOUT, call
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import re

def parseOption(argv):
    parser = OptionParser(version="%prog 1.0.0")
    parser.add_option("-e", "--environment", dest="env", help="input the environment in which the script needs to be executed ",
                        metavar="[prod|stg|...]")
   
    parser.add_option("-f", "--playbook", dest="pbook", help="input the command",
                        metavar="[ls|cd|...]")
   
    (options, args) = parser.parse_args()
    if not len(argv): parser.print_help();sys.exit(1) 
    return options 

def ansible_playbook_func(playbook_file,forks):
    ansible_cmd = "ansible-playbook %s -f %s" % (playbook_file,forks) 

    try:        
        pcmd = Popen(ansible_cmd, stdout=PIPE, stderr=STDOUT, shell=True)
        while True:
            for i in iter(pcmd.stdout.readline,b''):
                print i
            if pcmd.poll() is not None:

                break     
    except:
        exinfo=sys.exc_info()
        print exinfo
        return False
        
    


def main(argv):
    options = parseOption(argv)
    forks = 5
    playbook_file = options.pbook
#     playbook_file = "/opt/scripts/t1.yml"
    ansible_playbook_func(playbook_file,forks)
 
    

if __name__ == "__main__":
    main(sys.argv[1:])
    
