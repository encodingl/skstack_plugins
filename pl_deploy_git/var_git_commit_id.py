#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Part1:Load dependent library
from argparse import ArgumentParser
import sys
import os

# Part2:load skstack_plugins root path for load lib_pub
CONFIG_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from lib_pub.common import load_pri_json_conf
from pl_deploy_git.lib_pri.git import  get_git_commitid_by_command

def parseOption(argv):
    parser = ArgumentParser(description="version 2.0.0")

    parser.add_argument("-p", "--proj-git", dest="proj", metavar="[git_project_name]",
                        help="the static git project name you want to depoly")

    parser.add_argument("-e", "--environment", dest="env", metavar="[prod|stage|dev]",
                      help="the environment you need deploy ")
    
    parser.add_argument("-b", "--branch", dest="branch", metavar="[master|feature-xxx]",default="master",
                      help="the git branch you need deploy default=master ")

    args = parser.parse_args()
    if not len(argv): parser.print_help();sys.exit(1) 
    return args

def main(argv):
    options = parseOption(argv)
    env = options.env
    proj = options.proj
    branch = options.branch
    repo_url = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["repo_url"]
    proj_local_path = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["proj_local_path"]
    commit_lists = get_git_commitid_by_command(repo_url, proj_local_path,branch)
    print(commit_lists)

if __name__ == "__main__":
    main(sys.argv[1:])

