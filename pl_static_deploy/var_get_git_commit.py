#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2018年7月18日 @author: skipper
'''
import sys
from optparse import OptionParser
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from libSK.pythongit import  get_git_commitid_by_command



def parseOption(argv):
    parser = OptionParser(version="%prog 1.0.0")

    parser.add_option("-p", "--git-proj", dest="proj", metavar="[git_project_name]",
                        help="the static git project name you want to depoly")

    parser.add_option("-e", "--environment", dest="env", metavar="[prod|stg|dev]",
                      help="the environment you need deploy ")
    
    parser.add_option("-b", "--branch", dest="branch", metavar="[master|feature-xxx]",default="master",
                      help="the git branch you need deploy default=master ")

    (options, args) = parser.parse_args()
    if not len(argv):
        parser.print_help()
        sys.exit(1)
    return options

def main(argv):
    options = parseOption(argv)
    config_file = "static_conf_" + options.env
    exec ("from conf." + config_file + " import StaticProj")
    repo_url = StaticProj[options.proj]["repo_url"]
    proj_local_path = StaticProj[options.proj]["proj_local_path"]
    branch = options.branch

    commit_lists = get_git_commitid_by_command(repo_url, proj_local_path,branch)

    print(commit_lists)

if __name__ == "__main__":
    main(sys.argv[1:])

