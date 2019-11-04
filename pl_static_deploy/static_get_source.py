#! /usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import sys
import os
import re
from subprocess import Popen, PIPE, STDOUT, call

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from libSK.logger import sklog_init
sklog = sklog_init("static_deploy.log")

from libSK.pythongit import git_check_out_by_commit_num
from libSK.common import get_repo_file


def parseOption(argv):
    parser = OptionParser(version="%prog 1.0.0")

    parser.add_option("-p", "--git-proj", dest="proj", metavar="[git_project_name]",
                        help="the static git project name you want to depoly")

    parser.add_option("-e", "--environment", dest="env", metavar="[prod|stg|dev]",
                      help="the environment you need deploy ")

    parser.add_option("-i", "--commit-id", dest="id", metavar="[git_commit_id]",default="master",
                      help="the git commit id you want to depoly")

    parser.add_option("-f", "--file-name", dest="file", metavar="[file_name]",
                      help="the file name you want to depoly")

    (options, args) = parser.parse_args()
    if not len(argv):
        parser.print_help()
        sys.exit(1)
    return options


def main(argv):
    options = parseOption(argv)
    config_file = "static_conf_" + options.env
    exec ("from conf." + config_file + " import StaticProj")


    hosts = options.proj
    proj_type = StaticProj[options.proj]["type"]
    repo_url = StaticProj[options.proj]["repo_url"]
    proj_local_path = StaticProj[options.proj]["proj_local_path"]
    deploy_src_path = StaticProj[options.proj]["deploy_src_path"]
    deploy_dest_path = StaticProj[options.proj]["deploy_dest_path"]
    delete_enable = StaticProj[options.proj]["delete_enable"]
    owner = StaticProj[options.proj]["owner"]
    group = StaticProj[options.proj]["group"]
    if proj_type == "git_nodejs":
        commit_str = options.id
        pattern = re.compile(r'\w+')
        m = pattern.match(commit_str)
        commit_id = m.group(0)
        git_check_out_by_commit_num(repo_url, proj_local_path, commit_id)
    else:
        pass





if __name__ == "__main__":
    main(sys.argv[1:])

