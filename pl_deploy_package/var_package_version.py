#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Part1:Load dependent library
from argparse import ArgumentParser
import sys
import os
from bs4 import BeautifulSoup
import urllib.request
import re

# Part2:load skstack_plugins root path for load lib_pub
CONFIG_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from lib_pub.common import load_pri_json_conf

def parseOption(argv):
    parser = ArgumentParser(description="version 2.0.0")
    
    parser.add_argument("-e", "--environment", dest="env", metavar="[prod|stage|dev]",
                      help="the environment you need deploy ")
    parser.add_argument("-p", "--proj-package", dest="proj", metavar="[project_name]",
                        help="the static tar.gz project name you want to depoly")

    args = parser.parse_args()
    if not len(argv): parser.print_help();sys.exit(1) 
    return args

def main(argv):
    options = parseOption(argv)
    env = options.env
    proj = options.proj
    repo_url = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["repo_url"]
    url_response = urllib.request.urlopen(repo_url)
    html_doc = url_response.read()
    soup = BeautifulSoup(html_doc, "html.parser", from_encoding="utf-8")
    links = soup.find_all('a',href=re.compile(r"%s" % proj))
    
    tar_list=[]
    for link in links:
        tar_list.append(link['href'])
    tar_list.sort(reverse=True)
    print(tar_list)

if __name__ == "__main__":
    main(sys.argv[1:])