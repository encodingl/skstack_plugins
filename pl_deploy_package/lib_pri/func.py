#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

from lib_pub.logger import sklog_init

def get_repo_file(proj_type,repo_url,proj_local_path,version_id,log_file):
    sklog = sklog_init(log_file)
    if proj_type == "tar":

        wget_file_cmd = "wget %s%s" % (repo_url,version_id)
        if not os.path.exists(proj_local_path):
            os.makedirs(proj_local_path)
        else:
            pass

        if proj_local_path.startswith("/opt/tarsource/"):
            os.chdir(proj_local_path)
            sklog.info("clean up the old version ...")
            os.system("rm -rf *")
            sklog.info("clean job finished,wget the file ...")
            os.system(wget_file_cmd)
            sklog.info("wget job finished,extract file ...")
            os.system("tar xvf %s" % version_id)
            sklog.info("extract job finished ...")
        else:
            raise RuntimeError('You must config the var proj_local_path start with /opt/tarsource/')

    else:
        pass
    

