#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Part1:Load dependent library
from argparse import ArgumentParser
import sys
import os
import re
from subprocess import Popen, PIPE, STDOUT


# Part2:load skstack_plugins root path for load lib_pub
CONFIG_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


# Part3:load skstack lib_pub module 
from lib_pub.common import load_pri_json_conf,load_pub_json_conf
from lib_pub.logger import sklog_init
from lib_pub.common import get_repo_file
from pl_static_deploy.lib_pri.git import git_check_out_by_commit_num


# Part4:Define the script argument 
def parseOption(argv):
    parser = ArgumentParser(description="version 2.0.0")
    parser.add_argument("-p", "--git-proj", dest="proj", metavar="[git_project_name]",
                        help="the static git project name you want to depoly")
    parser.add_argument("-e", "--environment", dest="env", metavar="[prod|stg|dev]",
                      help="the environment you need deploy ")
    parser.add_argument("-i", "--commit-id", dest="id", metavar="[git_commit_id]",default="master",
                      help="the git commit id you want to depoly")
    parser.add_argument("-f", "--file-name", dest="file", metavar="[file_name]",
                      help="the file name you want to depoly")
    args = parser.parse_args()
    if not len(argv): parser.print_help();sys.exit(1) 
    return args

# Part5:Define the task function
def static_deploy(change_owner_tag,hosts,deploy_src_path,deploy_dest_path,delete_enable,owner,group,log_file):
    sklog = sklog_init(log_file)
    sklog.info("start deploy static files")
    if hosts in ["web-site","web-cms-app"]:
        ansible_cmd = "ansible-playbook static_sync.yml --tags php_frontend,%s -e \"hosts=%s deploy_src_path=%s  deploy_dest_path=%s delete_enable=%s owner=%s group=%s\" " % \
                  (change_owner_tag,hosts, deploy_src_path, deploy_dest_path, delete_enable,owner,group)
    else:
        ansible_cmd = "ansible-playbook static_sync.yml --tags common,%s -e \"hosts=%s deploy_src_path=%s  deploy_dest_path=%s delete_enable=%s owner=%s group=%s\" " % \
                      (change_owner_tag,hosts, deploy_src_path, deploy_dest_path, delete_enable, owner, group)
    try:
        pcmd = Popen(ansible_cmd, stdout=PIPE, stderr=STDOUT, shell=True)
    
        while True:
            for i in iter(pcmd.stdout.readline,b''):
                i=i.decode().strip('\n')
                if "FAILED" in i or " ERROR" in i:
                    sklog.error(i)
                else:
                    sklog.info(i)
            if pcmd.poll() is not None:
                break

    except:
        exinfo=sys.exc_info()
        sklog.error(exinfo)
    finally:
        retcode = pcmd.wait()
        if retcode == 0:
            pass
        else:
 
            raise Exception("task failed")

# Part6:Define the main function,accept parameters passed to the task function to executes
def main(argv):
    options = parseOption(argv)
    env = options.env
    hosts = options.proj
    proj = hosts
    log_path = load_pub_json_conf(env, "log_path")
    log_file = log_path + "static_deploy.log"
    proj_type = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["type"]
    repo_url = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["repo_url"]
    proj_local_path = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["proj_local_path"]
    deploy_src_path = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["deploy_src_path"]
    deploy_dest_path = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["deploy_dest_path"]
    delete_enable = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["delete_enable"]
    owner = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["owner"]
    group = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["group"]

    if proj_type == "git":
        commit_str = options.id
        pattern = re.compile(r'\w+')
        m = pattern.match(commit_str)
        commit_id = m.group(0)
        git_check_out_by_commit_num(repo_url, proj_local_path, commit_id)
    elif proj_type == "tar":
        version_id = options.file
        get_repo_file(proj_type,repo_url,proj_local_path,version_id)
    else:
        pass
    if deploy_src_path.endswith('/'):
        change_owner_tag = "dir_change_owner"
    else:
        change_owner_tag = "file_change_owner"

    
    os.chdir(CONFIG_BASE_DIR)
    static_deploy(change_owner_tag,hosts, deploy_src_path, deploy_dest_path, delete_enable,owner,group,log_file)



if __name__ == "__main__":
    main(sys.argv[1:])

