#! /usr/bin/env python
# -*- coding: utf-8 -*-

from git import Repo
import os
import subprocess
from lib_pub.logger import sklog_init

def makedirs_ignore_error(path, mode=0o777):
    '''调用 os.makedirs 但忽略 OSError 类型错误'''
    try:
        os.makedirs(path, mode)
    except OSError:
        pass
    return os.path.isdir(path)
def git_clone(git_url, repo_path):
    makedirs_ignore_error(repo_path)
    Repo.clone_from(url=git_url, to_path=repo_path)

def git_pull(repo_path,branch):
    subprocess.call(
        ['git', 'checkout', branch],
        cwd=repo_path,
        stderr=subprocess.STDOUT, stdout=subprocess.PIPE)

    subprocess.call(
        ['git', 'pull'],
        cwd=repo_path,
        stderr=subprocess.STDOUT, stdout=subprocess.PIPE)

def get_git_commitid(git_url, repo_path, num=10, git_commit=''):
    if not os.path.isdir(repo_path):
        git_clone(git_url,repo_path)

    git_pull(repo_path)

    g = Repo(repo_path, search_parent_directories=True)
    list_commitid=g.iter_commits("master", max_count=num)

    list_tumple_commitid = []

    for l in list_commitid:
        l = str(l)
        # 获取commit 号的前7位
        l=l[0:7]
        t1=(l)
        list_tumple_commitid.append(t1)

    return list_tumple_commitid

def git_check_out_by_commit_num(git_url, repo_path, git_commit,log_file):
    sklog = sklog_init(log_file)
    if not os.path.isdir(repo_path):
        git_clone(git_url,repo_path)

#     git_pull(repo_path)
    subprocess.call(
        ['git', 'pull'],
        cwd=repo_path,
        stderr=subprocess.STDOUT, stdout=subprocess.PIPE)

    # Git: fatal: Unable to create '.git/index.lock': File exists.
    subprocess.Popen(
        ['rm', '-f', '.git/index.lock'],
        cwd=repo_path,
        stderr=subprocess.STDOUT, stdout=subprocess.PIPE)

    check_info = subprocess.Popen(
        ['git', 'checkout', git_commit],
        cwd=repo_path,
        stderr=subprocess.STDOUT, stdout=subprocess.PIPE)

    sklog.info(check_info.stdout.readline().decode())

def get_git_commitid_by_command(git_url, repo_path, branch,num=10, git_commit=''):
    if not os.path.isdir(repo_path):
        git_clone(git_url,repo_path)

    git_pull(repo_path,branch)

    list_commitid = subprocess.Popen(
        ['git', 'log', '--pretty=format:%h (%cr)  %ce %s', '-10'],
        cwd=repo_path,
        stderr=subprocess.STDOUT, stdout=subprocess.PIPE)

    list_tumple_commitid = [x.decode().strip('\n') for x in list_commitid.stdout.readlines() if x is not None]
    return list_tumple_commitid
