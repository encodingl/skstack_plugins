#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Part1:Load dependent library
from argparse import ArgumentParser
import sys
import os
from subprocess import Popen, PIPE, STDOUT
import datetime

# Part2:load skstack_plugins root path for load lib_pub
CONFIG_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


# Part3:load skstack lib_pub module 
from lib_pub.common import load_pri_json_conf,load_pub_json_conf
from lib_pub.logger import sklog_original

# Part4:Define the script argument 
def parseOption(argv):
    parser = ArgumentParser(description="version 2.0.0")
    parser.add_argument("-e", "--environment", dest="env", help="input the environment in which the script needs to be executed ",
                        metavar="[prod|stage|dev|...]")
    parser.add_argument("-g", "--group", dest="group", help="input the ansible hosts group",
                        metavar="[gp01|ip|...]")
    parser.add_argument("-c", "--command", dest="cmd", help="input the command",
                        metavar="[ls|cd|...]")
   
    args = parser.parse_args()
    if not len(argv): parser.print_help();sys.exit(1) 
    return args 

# Part5:Define the task function
def ansible_cmd_func(hosts,forks,cmd,log_file):
    sklog = sklog_original(log_file)
    ansible_cmd = "ansible %s -f %s  -m shell -a '%s' " % (hosts,forks,cmd)
    sklog.info("%s INFO the ansible shell task started" % datetime.datetime.now())
    try:        
        pcmd = Popen(ansible_cmd, stdout=PIPE, stderr=STDOUT, shell=True) 
        while True: 
            line = pcmd.stdout.readline().strip() 
            if line:
                line = str(line,encoding='utf-8')
                sklog.info(line)
            else:
                break   
        
    except:
        exinfo=sys.exc_info()
        sklog.error(exinfo)
    
    retcode = pcmd.wait()
    if retcode == 0:
        sklog.info("%s INFO the ansible shell task finished" % datetime.datetime.now())
    else:
        raise Exception("Command failed")
    
# Part6:Define the main function,accept parameters passed to the task function to executes
def main(argv):
    options = parseOption(argv)
    hosts = options.group
    cmd = options.cmd
    env = options.env
    forks = load_pri_json_conf(CONFIG_BASE_DIR,env, "forks")
    log_path = load_pub_json_conf(env, "log_path")
    log_file = log_path + "ansible_shell.log"
    ansible_cmd_func(hosts,forks,cmd,log_file)
 
    

if __name__ == "__main__":
  
    main(sys.argv[1:])
    
