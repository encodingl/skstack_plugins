#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Part1:Load dependent library
from argparse import ArgumentParser
import sys
import os

# Part2:load skstack_plugins env to sys
CONFIG_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Part3:load skstack lib_pub module
from lib_pub.common import load_pri_json_conf


# Part4:Define optional variables
def parseOption(argv):
    parser = ArgumentParser(description="version 2.0.0")
    parser.add_argument("-e", "--environment", dest="env", metavar="[prod|stage|...]",
                        help="the environment you need deploy ")

    parser.add_argument("-p", "--proj-package", dest="proj", metavar="[project_name]",
                        help="the ansible project name you want to depoly")


    args = parser.parse_args()
    if not len(argv): parser.print_help();sys.exit(1)
    return args


# Part5:Define the task function
def get_AnsiblePlaybookFile(ansible_playbook_path):
    file_list = []

    # all_files 包含了该目录下面包括子目录里面的所有文件，另外如果有子目录，名字也不能相同，不过已经定义好不要子目录了。
    for root_dirs, sub_dirs, all_files in os.walk(ansible_playbook_path):
        for f in all_files:
            file_list.append(f)

    list_plyabook_file = file_list
    return list_plyabook_file


# Part6:Define the main function,accept parameters passed to the task function to executes
def main(argv):
    options = parseOption(argv)
    env = options.env
    proj = options.proj

    ansible_playbook_path = load_pri_json_conf(CONFIG_BASE_DIR, env, proj)["playbook_path"]
    list_plyabook_file = get_AnsiblePlaybookFile(ansible_playbook_path)
    print(list_plyabook_file)



if __name__ == "__main__":
    main(sys.argv[1:])
