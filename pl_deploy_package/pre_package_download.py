#! /usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import sys
import os


# Part2:load skstack_plugins root path for load lib_pub
CONFIG_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Part3:load skstack lib_pub module 
from lib_pub.common import load_pri_json_conf,load_pub_json_conf
from pl_deploy_package.lib_pri.func import get_repo_file

def parseOption(argv):
    parser = ArgumentParser(description="version 2.0.0")
    parser.add_argument("-p", "--git-proj", dest="proj", metavar="[git_project_name]",
                        help="the static git project name you want to depoly")
    parser.add_argument("-e", "--environment", dest="env", metavar="[prod|stage|dev]",
                      help="the environment you need deploy ")
    parser.add_argument("-f", "--file-name", dest="file", metavar="[file_name]",
                      help="the file name you want to depoly")
    args = parser.parse_args()
    if not len(argv): parser.print_help();sys.exit(1) 
    return args


def main(argv):
    options = parseOption(argv)
    env = options.env
    hosts = options.proj
    proj = hosts
    log_path = load_pub_json_conf(env, "log_path")
    log_file = log_path + "pl_deploy_package.log"
    proj_type = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["type"]
    repo_url = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["repo_url"]
    proj_local_path = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["proj_local_path"]
    version_id = options.file
    get_repo_file(proj_type,repo_url,proj_local_path,version_id,log_file)






if __name__ == "__main__":
    main(sys.argv[1:])

