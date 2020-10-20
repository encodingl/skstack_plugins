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

from lib_pub.common import load_pri_json_conf_keys


def parseOption(argv):
    parser = ArgumentParser(description="version 2.0.0")

    parser.add_argument("-k", "--filter-keyword", dest="keyword", metavar="[keyword1|keyword2]", default="None",
                        help="the project keyword you want to filter")

    parser.add_argument("-d", "--exclude", dest="exclude", metavar="[keyword1|keyword2]", default="None",
                        help="Exclude what you don’t want, but you can only use it after the keyword is enabled ")

    parser.add_argument("-e", "--environment", dest="env", metavar="[prod|stage|dev]",
                      help="the environment you need deploy ")



    

    args = parser.parse_args()
    if not len(argv): parser.print_help();sys.exit(1) 
    return args

def main(argv):
    options = parseOption(argv)
    env = options.env
    keyword = options.keyword
    exclude = options.exclude
   
    list_keys = load_pri_json_conf_keys(CONFIG_BASE_DIR, env, keyword, exclude)
    
    print(list_keys)

if __name__ == "__main__":
    main(sys.argv[1:])

