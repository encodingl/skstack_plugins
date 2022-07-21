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
from pl_deploy_docker.lib_pri.docker_info import  docker_aliyun_repo_tags
from pl_deploy_docker.lib_pri.docker_info import  docker_gcp_repo_list_tags

def parseOption(argv):
    parser = ArgumentParser(description="version 2.0.0")

    parser.add_argument("-p", "--proj-docker", dest="proj", metavar="[project_name]",
                        help="the project name you want to depoly")

    parser.add_argument("-e", "--environment", dest="env", metavar="[prod|stage|dev]",
                      help="the environment you need deploy ")

    parser.add_argument("-ns", "--repo-namespace", dest="repo_namespace", metavar="[repo_namespace]",
                        help="the register repo namespace you want to depoly")

    parser.add_argument("-n", "--repo-name", dest="repo_name", metavar="[",
                      help="the register repo name you want to depoly")

    parser.add_argument("-r", "--region-id", dest="region_id", metavar="[]",
                      help="the register region id you want to depoly ")

    parser.add_argument("-ak", "--access-key", dest="access_key", metavar="[]",
                      help="if you use aliyun, the register access key you want to depoly")

    parser.add_argument("-as", "--access-secret", dest="access_secret", metavar="[]",
                      help="if you use aliyun, the register access secret you want to depoly")

    parser.add_argument("-ps", "--pagesize", dest="pagesize", metavar="[10|20]",default="20",
                      help="if you use aliyun, the register search how size you want to depoly")

    parser.add_argument("-k", "--key-json", dest="key_json", metavar="[]",
                      help="if you use gcp artifact-registry, the register key json you want to depoly ")

    parser.add_argument("-g", "--gcp-projects", dest="gcp_proj", metavar="[]",
                      help="if you use gcp artifact-registry, the register gcp projects you want to depoly ")

    parser.add_argument("-pr", "--provider", dest="provider", metavar="[gcp|aliyun|aws]",
                      help="if you use register type to provider, the register type you want to depoly ")                          

    args = parser.parse_args()
    if not len(argv): parser.print_help();sys.exit(1) 
    return args

def main(argv):
    options = parseOption(argv)
    proj = options.proj
    env = options.env
    repo_namespace = options.repo_namespace
    repo_name = options.repo_name
    pagesize = options.pagesize
    region_id = options.region_id

    provider = options.provider

    if provider == "aliyun":        
        access_key = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["access_key"]
        access_secret = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["access_secret"]
        docker_tags_lists = docker_aliyun_repo_tags(repo_namespace, repo_name,access_key,access_secret,region_id,pagesize)
    elif provider == "gcp":
        key_json_path = os.path.join(CONFIG_BASE_DIR,"conf",options.key_json)
        gcp_proj = options.gcp_proj
        docker_tags_lists = docker_gcp_repo_list_tags(key_json_path,gcp_proj,region_id,repo_namespace, repo_name,pagesize)
    
    print(docker_tags_lists)

if __name__ == "__main__":
    main(sys.argv[1:])

