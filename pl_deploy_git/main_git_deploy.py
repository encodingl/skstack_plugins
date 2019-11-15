#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Part1:Load dependent library
from argparse import ArgumentParser
import sys
import os
from subprocess import Popen, PIPE, STDOUT


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
    parser.add_argument("-p", "--proj-git", dest="proj", metavar="[git_project_name]",
                        help="the static git project name you want to depoly")
    
    
 
    args = parser.parse_args()
    if not len(argv): parser.print_help();sys.exit(1) 
    return args

# Part5:Define the task function
def static_deploy(change_owner_tag,hosts,deploy_src_path,deploy_dest_path,delete_enable,owner,group,log_file,rsync_opts):
    sklog = sklog_original(log_file)
    sklog.info("start deploy static files")
    vars_dic = {
        "hosts":hosts,
        "deploy_src_path":deploy_src_path,
        "deploy_dest_path":deploy_dest_path,
        "delete_enable":delete_enable,
        "owner":owner,
        "group":group,
        "rsync_opts":rsync_opts
        }
    ansible_cmd = "ansible-playbook sc_static_sync.yml --tags common,%s -e '%s' " % (change_owner_tag,vars_dic)
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
        sklog.error(exinfo)
    finally:
        retcode = pcmd.wait()
        if retcode == 0:
            pass
        else:
 
            raise Exception("task failed")

# Part6:Define the main function,accept parameters passed to the task function to executes
def main(argv):
    options = parseOption(argv)
    env = options.env
    hosts = options.proj
    proj = hosts
    log_path = load_pub_json_conf(env, "log_path")
    log_file = log_path + "pl_deploy_git.log"
   
    deploy_src_path = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["deploy_src_path"]
    rsync_opts = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["rsync_opts"]
    deploy_dest_path = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["deploy_dest_path"]
    delete_enable = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["delete_enable"]
    owner = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["owner"]
    group = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["group"]


    if deploy_src_path.endswith('/'):
        change_owner_tag = "dir_change_owner"
    else:
        change_owner_tag = "file_change_owner"

    
    os.chdir(CONFIG_BASE_DIR)
    static_deploy(change_owner_tag,hosts, deploy_src_path, deploy_dest_path, delete_enable,owner,group,log_file,rsync_opts)



if __name__ == "__main__":
    main(sys.argv[1:])

