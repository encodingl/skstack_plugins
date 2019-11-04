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
from bs4 import BeautifulSoup
import urllib2
import re

def parseOption(argv):
    parser = OptionParser(version="%prog 1.0.0")

    parser.add_option("-p", "--tar-proj", dest="proj", metavar="[tar_project_name]",
                        help="the static tar.gz project name you want to depoly")

    parser.add_option("-e", "--environment", dest="env", metavar="[prod|stg|dev]",
                      help="the environment you need deploy ")

    (options, args) = parser.parse_args()
    if not len(argv):
        parser.print_help()
        sys.exit(1)
    return options

def main(argv):
    options = parseOption(argv)
    config_file = "static_conf_" + options.env
    exec ("from conf." + config_file + " import StaticProj")
    proj = options.proj
    repo_url = StaticProj[proj]["repo_url"]

    url_response = urllib2.urlopen(repo_url)
    html_doc = url_response.read()
    soup = BeautifulSoup(html_doc, "html.parser", from_encoding="utf-8")
    if proj == "app_h5":
        links = soup.find_all('a',href=re.compile(r"app-"))
    elif proj == "appT_h5":
        links = soup.find_all('a',href=re.compile(r"appT-"))
    else:
        links = soup.find_all('a')
    tar_list=[]
    for link in links:
        tar_list.append(link['href'])
    tar_list.sort(reverse=True)
    print tar_list

if __name__ == "__main__":
    main(sys.argv[1:])


