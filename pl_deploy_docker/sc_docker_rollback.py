#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
pre_deploy:
1 init vars in conf:docker run cmd for app;
2 Get the project list and tag for app from docker image warehouse
3 input:appname apptag imageurl


ansible deploy tasks:
1 check service status
2 download docker image
3 deregister
4 docker stop
5 docker run
6 check service status
7 security wait times

after_deploy:
1 custom health check for app instance
2 sms notify someone
"""
from optparse import OptionParser
import sys
import os
from subprocess import Popen, PIPE, STDOUT, call

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import re
import time

from libSK.logger import sklog_init
sklog = sklog_init("mitra_docker_rollback.log")

# logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s msg:%(message)s')
# log = logging.getLogger(__name__)


def parseOption(argv):
    parser = OptionParser(version="%prog 1.0.0")
    parser.add_option("-e", "--Environment", dest="env",
                      help="input the environment in which the script needs to be executed ",
                      metavar="[prod|stage|dev...]")
    parser.add_option("-a", "--DockerAppName", dest="app", help="input the appname for docker",
                      metavar="[app01|app02|...]")
    parser.add_option("-n", "--DockerRollBackName", dest="name", help="input the docker run name you need to rollback",
                      metavar="[app01-time| app02-20190531.123225|...]")
    parser.add_option("-i", "--AnsibleHosts", dest="hosts", help="input AnsibleHosts ,default is the same as -a parameter",default="options.app",
                      metavar="[192.168.1.22|AnsbileHostsName|...]")
    parser.add_option("-w", "--WaitTimes", dest="times", help="input  wait times for spring service register default=60s",default="60s",
                      metavar="[3s|1m|...]")

    parser.add_option("-m", "--RollBackMode", dest="mode", help="input RollBack Mode,you need choose the DockerRollBackName in manual mode, default=auto",
                      default="auto",
                      metavar="[auto|manual]")
    parser.add_option("-s", "--PlaybookSerial", dest="serial",default=1,
                      help="input Concurrency number for this rollback task,default=1",
                      metavar="[number|1|2|...]")

    (options, args) = parser.parse_args()
    if not len(argv): parser.print_help();sys.exit(1)
    return options


def ansible_rollback(mode,hosts,serial,app,docker_rollback_name,wait_times,eureka_url,app_spring_name):
    if app_spring_name == "null":
        ansible_cmd = "ansible-playbook rollback.yml --tags %s -v  -e \"hosts=%s serial=%s DockerApp=%s DockerName=%s  WaitTimes=%s EurekaUrl=%s AppSpringName=%s\" " % \
                      (mode,hosts,serial,app,docker_rollback_name,wait_times,eureka_url,app_spring_name)
    else:
        ansible_cmd = "ansible-playbook rollback.yml --tags %s,eureka -v  -e \"hosts=%s serial=%s DockerApp=%s DockerName=%s  WaitTimes=%s EurekaUrl=%s AppSpringName=%s\" " % \
                      (mode, hosts, serial, app, docker_rollback_name, wait_times, eureka_url, app_spring_name)
    try:
        pcmd = Popen(ansible_cmd, stdout=PIPE, stderr=PIPE, shell=True)
        while True:
            for i in iter(pcmd.stdout.readline,b''):
                i=i.strip('\n')

                if "FAILED" in i:
                    sklog.error(i)
                elif "Error" in i:
                    sklog.warning(i)

                else:
                    sklog.info(i)


            if pcmd.poll() is not None:
                break
    except:
        exinfo=sys.exc_info()
        # print exinfo
        sklog.error(exinfo)
        return False


def main(argv):
    options = parseOption(argv)
    mode = options.mode
    serial = options.serial
    config_file = "mitra_conf_"+options.env
    exec("from conf."+config_file+ " import MitraVars")
    app = options.app
    docker_rollback_name = options.name
    wait_times = options.times
    hosts = options.hosts
    if hosts == "options.app":
        hosts = app
    eureka_url = MitraVars["EurekaUrl"]

    app_spring_name = MitraVars[options.app]["AppSpringName"]
    ansible_rollback(mode,hosts,serial,app,docker_rollback_name,wait_times,eureka_url,app_spring_name)



if __name__ == "__main__":
    main(sys.argv[1:])



