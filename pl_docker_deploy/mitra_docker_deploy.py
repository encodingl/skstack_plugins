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

import time

from libSK.logger import sklog_init
sklog = sklog_init("mitra_docker_deploy.log")


def parseOption(argv):
    parser = OptionParser(version="%prog 1.0.0")
    parser.add_option("-e", "--Environment", dest="env",
                      help="input the environment in which the script needs to be executed ",
                      metavar="[prod|stg|dev...]")
    parser.add_option("-a", "--DockerAppName", dest="app", help="input the appname for docker",
                      metavar="[app01|app02|...]")
    parser.add_option("-t", "--DockerImageTag", dest="tag", help="input the docker image tag default=latest",default="latest",
                      metavar="[v0.1.0|latest|...]")
    parser.add_option("-i", "--AnsibleHosts", dest="hosts", help="input AnsibleHosts,default is the same as -a parameter",default="options.app",
                      metavar="[192.168.1.22|AnsbileHostsName|...]")
    parser.add_option("-w", "--WaitTimes", dest="times", help="input securyty wait times for rolling update default=60s",default="60s",
                      metavar="[3s|1m|...]")
    parser.add_option("-m", "--ExecMode", dest="mode", help="input the execution mode you need",
                      metavar="[update|restart|inquiry|rollback|update_hard]")

    (options, args) = parser.parse_args()
    if not len(argv): parser.print_help();sys.exit(1)
    return options


def ansible_deploy(hosts,app,tag,docker_run,docker_image_url,wait_times,eureka_url,app_spring_name,exec_mode):
    if app_spring_name == "null":
        if exec_mode == "update":
            ansible_cmd = "ansible-playbook update_NoEurekaApp.yml -v -e \"hosts=%s DockerApp=%s DockerImageTag=%s DockerRun='%s' DockerImageURL=%s  AppSpringName=%s\" " % \
                      (hosts, app, tag, docker_run, docker_image_url, app_spring_name)
        elif exec_mode == "restart":
            ansible_cmd = "ansible-playbook restart.yml --skip-tags 'eureka' -v -e \"hosts=%s DockerApp=%s\" " % (hosts, app)
        elif exec_mode == "rollback":
            ansible_cmd = "ansible-playbook rollback.yml --skip-tags eureka,manual -v  -e \"hosts=%s serial=1 DockerApp=%s   WaitTimes=%s EurekaUrl=%s AppSpringName=%s\" " % \
                          (hosts, app, wait_times, eureka_url, app_spring_name)
        elif exec_mode == "inquiry":
            ansible_cmd = "ansible %s -m shell -a \"docker ps -a|egrep '%s[\ |:]|NAMES' \" " % \
                          (hosts, app)
        elif exec_mode == "update_hard":
            ansible_cmd = "ansible-playbook update_NoEurekaApp.yml -v -e \"hosts=%s DockerApp=%s DockerImageTag=%s DockerRun='%s' DockerImageURL=%s\" " % \
                          (hosts, app, tag, docker_run, docker_image_url)
        else:
            
            sklog.error("please choose the ExecMode ")
            exit(1)
         

    else:
        if exec_mode == "update":
            ansible_cmd = "ansible-playbook update_EurekaApp.yml -v -e \"hosts=%s DockerApp=%s DockerImageTag=%s DockerRun='%s' DockerImageURL=%s WaitTimes=%s EurekaUrl=%s AppSpringName=%s\" " % \
                  (hosts,app,tag,docker_run,docker_image_url,wait_times,eureka_url,app_spring_name)
        elif exec_mode == "restart":
            ansible_cmd = "ansible-playbook restart.yml -v -e \"hosts=%s DockerApp=%s WaitTimes=%s EurekaUrl=%s  AppSpringName=%s\" " % (hosts, app,wait_times,eureka_url,app_spring_name)
        elif exec_mode == "rollback":
            ansible_cmd = "ansible-playbook rollback.yml --skip-tags manual -v  -e \"hosts=%s DockerApp=%s  serial=1 WaitTimes=%s EurekaUrl=%s AppSpringName=%s\" " % \
                          (hosts, app, wait_times, eureka_url, app_spring_name)
        elif exec_mode == "inquiry":
            ansible_cmd = "ansible %s -m shell -a \"docker ps -a|egrep '%s[\ |:]|NAMES' \" " % \
                          (hosts, app)
        elif exec_mode == "update_hard":
            ansible_cmd = "ansible-playbook update_NoEurekaApp.yml -v -e \"hosts=%s DockerApp=%s DockerImageTag=%s DockerRun='%s' DockerImageURL=%s\" " % \
                          (hosts, app, tag, docker_run, docker_image_url)
        else:
            sklog.error("please choose the ExecMode ")
            exit(1)
           

    try:
        pcmd = Popen(ansible_cmd, stdout=PIPE, stderr=STDOUT, shell=True)
        if exec_mode in ["inquiry",]:
            while True:
                line = pcmd.stdout.readline().strip()
                if line:
                    print(line)
                else:
                    break
        else:
            while True:
                for i in iter(pcmd.stdout.readline,b''):
                    i=i.strip('\n')
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




def main(argv):
    options = parseOption(argv)
    config_file = "mitra_conf_"+options.env
    exec("from conf."+config_file+ " import MitraVars")
    app = options.app
    tag = options.tag
    hosts = options.hosts
    wait_times = options.times
    exec_mode = options.mode
    if hosts == "options.app":
        hosts = app
    docker_image_url = MitraVars["DockerImageURL"]
    eureka_url = MitraVars["EurekaUrl"]
    docker_run_image = "%s%s:%s" % (docker_image_url,app,tag)
    docker_run_arg = MitraVars[options.app]["DockerRunArg"]
    if  "DockerRunCmd" in MitraVars[options.app]:
        docker_run_cmd = MitraVars[options.app]["DockerRunCmd"]
    else :
        docker_run_cmd = "";
    docker_run_time = time.strftime("%Y%m%d.%H%M%S", time.localtime())
    docker_run_name = "%s-%s" % (app,docker_run_time)
    docker_run_arg = "--name %s %s" % (docker_run_name,docker_run_arg)
    docker_run = "docker run  %s %s %s" % (docker_run_arg,docker_run_image,docker_run_cmd)
    app_spring_name = MitraVars[options.app]["AppSpringName"]
    work_path = "%s/scApplication/" % BASE_DIR
    os.chdir(work_path)

    ansible_deploy(hosts,app,tag,docker_run,docker_image_url,wait_times,eureka_url,app_spring_name,exec_mode)



if __name__ == "__main__":
    main(sys.argv[1:])



