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
    parser.add_argument("-e", "--environment", dest="env", metavar="[prod|stage|dev]",
                        help="the environment you need deploy ")
    parser.add_argument("-p", "--project-name", dest="proj", metavar="[proj1|proj2]",
                        help="the  project name you want to depoly")
    parser.add_argument("-f", "--playbook", dest="pbook", metavar="playbook_name.yml",
                        help="input the command")
    parser.add_argument("-a", "--ansible-hosts", dest="hosts", metavar="[ansible-hosts]",default="none",
                        help="the destination hosts you want to depoly")
    args = parser.parse_args()
    if not len(argv): parser.print_help();sys.exit(1)
    return args

# Part5:Define the task function
def ansible_playbook_func(playbook_file,playbook_path,hosts,serial,log_file):
    sklog = sklog_original(log_file)
    sklog.info("%s INFO the ansible playbook task started" % datetime.datetime.now())
    vars_dic = {
        "hosts": hosts,
        "serial": serial
        }

    ansible_cmd = "ansible-playbook %s/%s -e '%s'" % (playbook_path, playbook_file, vars_dic)
    try:        
        pcmd = Popen(ansible_cmd, stdout=PIPE, stderr=STDOUT, shell=True)
        while True:
            for i in iter(pcmd.stdout.readline,b''):
                i=i.decode().strip('\n')
                if "FAILED" in i or " ERROR" in i:
                    sklog.error(i)
                else:
                    sklog.info(i)
            if pcmd.poll() is not None:
                break
    except:
        exinfo=sys.exc_info()
        print(exinfo)
        sklog.error(exinfo)
        # return False
    finally:
        retcode = pcmd.wait()
        if retcode == 0:
            pass
        else:
            raise Exception("task failed,please check pl_ansible_playbook.log for details")


# Part6:Define the main function,accept parameters passed to the task function to executes
def main(argv):
    options = parseOption(argv)
    env = options.env
    proj = options.proj
    playbook_file = options.pbook

    opt_hosts = options.hosts
    json_hosts = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["hosts"]
    if opt_hosts != "none":
        hosts = opt_hosts
    elif opt_hosts == "none" and json_hosts != "none":
        hosts = json_hosts
    else:
        hosts = proj

    log_path = load_pub_json_conf(env, "log_path")
    log_file = log_path + "pl_deploy_ansible_playbook.log"

    serial = load_pri_json_conf(CONFIG_BASE_DIR, env, proj)["serial"]
    playbook_path = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["playbook_path"]

    os.chdir(CONFIG_BASE_DIR)
    ansible_playbook_func(playbook_file,playbook_path,hosts,serial,log_file)
 


if __name__ == "__main__":
    main(sys.argv[1:])
    
