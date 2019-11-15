#! /usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import sys
import os
import re

# Part2:load skstack_plugins root path for load lib_pub
CONFIG_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Part3:load skstack lib_pub module 
from lib_pub.common import load_pri_json_conf,load_pub_json_conf
from pl_deploy_git.lib_pri.git import git_check_out_by_commit_num



def parseOption(argv):
    parser = ArgumentParser(description="version 2.0.0")

    parser.add_argument("-p", "--git-proj", dest="proj", metavar="[git_project_name]",
                        help="the static git project name you want to depoly")

    parser.add_argument("-e", "--environment", dest="env", metavar="[prod|stage|dev]",
                      help="the environment you need deploy ")

    parser.add_argument("-i", "--commit-id", dest="id", metavar="[git_commit_id]",default="master",
                      help="the git commit id you want to depoly")



    args = parser.parse_args()
    if not len(argv): parser.print_help();sys.exit(1) 
    return args


def main(argv):
    options = parseOption(argv)
    env = options.env
    hosts = options.proj
    proj = hosts
    
    log_path = load_pub_json_conf(env, "log_path")
    log_file = log_path + "pl_deploy_git.log"
    

    proj_type = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["type"]
    repo_url = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["repo_url"]
    proj_local_path = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["proj_local_path"]

    if proj_type == "git":
        commit_str = options.id
        pattern = re.compile(r'\w+')
        m = pattern.match(commit_str)
        commit_id = m.group(0)
        git_check_out_by_commit_num(repo_url, proj_local_path, commit_id,log_file)
    else:
        pass





if __name__ == "__main__":
    main(sys.argv[1:])

