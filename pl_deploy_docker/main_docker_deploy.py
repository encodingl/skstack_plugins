#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
pre_deploy:
1 init vars in conf:docker run cmd for proj;
2 Get the project list and tag for proj from docker image warehouse
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
1 custom health check for proj instance
2 sms notify someone
"""

# Part1:Load dependent library
from argparse import ArgumentParser
import sys,os,time
from subprocess import Popen, PIPE, STDOUT

# Part2:load skstack_plugins root path 
CONFIG_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


# Part3:load skstack lib_pub and lib_pri module 
from lib_pub.common import load_pri_json_conf,load_pub_json_conf
from lib_pub.logger import sklog_init



def parseOption(argv):
    parser = ArgumentParser(description="version 2.0.0")
    parser.add_argument("-e", "--Environment", dest="env",
                      help="input the environment in which the script needs to be executed ",
                      metavar="[prod|stage|dev...]")
    parser.add_argument("-p", "--proj-docker", dest="proj", metavar="[proj01|proj02|...]",
                        help="the docker project you want to depoly")
    parser.add_argument("-t", "--DockerImageTag", dest="tag", help="input the docker image tag default=latest",default="latest",
                      metavar="[v0.1.0|latest|...]")
    parser.add_argument("-a", "--AnsibleHosts", dest="hosts", help="input AnsibleHosts,default is the same as -p parameter",default="none",
                      metavar="[192.168.1.22|AnsbileHostsName|...]")
    parser.add_argument("-w", "--WaitTimes", dest="times", help="input securyty wait times for rolling update default=60s",default="60s",
                      metavar="[3s|1m|...]")
    parser.add_argument("-m", "--ExecMode", dest="mode", help="input the execution mode you need",
                      metavar="[update|restart|inquiry|rollback|update_hard]")

    args = parser.parse_args()
    if not len(argv): parser.print_help();sys.exit(1) 
    return args



def docker_deploy(hosts,proj,tag,docker_run,docker_image_url,wait_times,eureka_url,app_spring_name,exec_mode,log_file):
    sklog = sklog_init(log_file)
    if app_spring_name == "null":
        if exec_mode == "update":
            ansible_cmd = "ansible-playbook sc_update_hard.yml -v -e \"hosts=%s DockerApp=%s DockerImageTag=%s DockerRun='%s' DockerImageURL=%s  AppSpringName=%s\" " % \
                      (hosts, proj, tag, docker_run, docker_image_url, app_spring_name)
        elif exec_mode == "restart":
            ansible_cmd = "ansible-playbook sc_restart.yml --skip-tags 'eureka' -v -e \"hosts=%s DockerApp=%s\" " % (hosts, proj)
        elif exec_mode == "rollback":
            ansible_cmd = "ansible-playbook sc_rollback.yml --skip-tags eureka,manual -v  -e \"hosts=%s serial=1 DockerApp=%s   WaitTimes=%s EurekaUrl=%s AppSpringName=%s\" " % \
                          (hosts, proj, wait_times, eureka_url, app_spring_name)
        elif exec_mode == "inquiry":
            ansible_cmd = "ansible %s -m shell -a \"docker ps -a|egrep '%s[\ |:]|NAMES' \" " % \
                          (hosts, proj)
        elif exec_mode == "update_hard":
            ansible_cmd = "ansible-playbook sc_update_hard.yml -v -e \"hosts=%s DockerApp=%s DockerImageTag=%s DockerRun='%s' DockerImageURL=%s\" " % \
                          (hosts, proj, tag, docker_run, docker_image_url)
        else:
            
            sklog.error("please choose the ExecMode ")
            exit(1)
         
    else:
        if exec_mode == "update":
            ansible_cmd = "ansible-playbook sc_update_soft.yml -v -e \"hosts=%s DockerApp=%s DockerImageTag=%s DockerRun='%s' DockerImageURL=%s WaitTimes=%s EurekaUrl=%s AppSpringName=%s\" " % \
                  (hosts,proj,tag,docker_run,docker_image_url,wait_times,eureka_url,app_spring_name)
        elif exec_mode == "restart":
            ansible_cmd = "ansible-playbook sc_restart.yml -v -e \"hosts=%s DockerApp=%s WaitTimes=%s EurekaUrl=%s  AppSpringName=%s\" " % (hosts, proj,wait_times,eureka_url,app_spring_name)
        elif exec_mode == "rollback":
            ansible_cmd = "ansible-playbook sc_rollback.yml --skip-tags manual -v  -e \"hosts=%s DockerApp=%s  serial=1 WaitTimes=%s EurekaUrl=%s AppSpringName=%s\" " % \
                          (hosts, proj, wait_times, eureka_url, app_spring_name)
        elif exec_mode == "inquiry":
            ansible_cmd = "ansible %s -m shell -a \"docker ps -a|egrep '%s[\ |:]|NAMES' \" " % \
                          (hosts, proj)
        elif exec_mode == "update_hard":
            ansible_cmd = "ansible-playbook sc_update_hard.yml -v -e \"hosts=%s DockerApp=%s DockerImageTag=%s DockerRun='%s' DockerImageURL=%s\" " % \
                          (hosts, proj, tag, docker_run, docker_image_url)
        else:
            sklog.error("please choose the Exec Mode ")
            exit(1)
           

    try:
        pcmd = Popen(ansible_cmd, stdout=PIPE, stderr=STDOUT, shell=True)
        if exec_mode in ["inquiry",]:
            while True:
                for line in iter(pcmd.stdout.readline,b''):
#                 line = pcmd.stdout.readline().strip()
                    if line:
                        sklog.info(line)
                    else:
                        break
        else:
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
            raise Exception("task failed,please check pl_deploy_docker.log for details")

def main(argv):
    options = parseOption(argv)
    env = options.env
    log_path = load_pub_json_conf(env, "log_path")
    log_file = log_path + "pl_deploy_docker.log"
    proj = options.proj
    tag = options.tag
    wait_times = options.times
    exec_mode = options.mode
  
    opt_hosts = options.hosts
    json_hosts = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["hosts"]
    if opt_hosts != "none" :
        hosts = opt_hosts
    elif opt_hosts == "none" and json_hosts != "none":
        hosts = json_hosts
    else:
        hosts = proj
        
    docker_image_url = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["DockerImageURL"]
    eureka_url = load_pri_json_conf(CONFIG_BASE_DIR,env, "public")["EurekaUrl"]
    docker_run_arg = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["DockerRunArg"]
    docker_run_cmd = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["DockerRunCmd"]
    app_spring_name = load_pri_json_conf(CONFIG_BASE_DIR,env, proj)["AppSpringName"]
    docker_run_image = "%s%s:%s" % (docker_image_url,proj,tag)
    docker_run_time = time.strftime("%Y%m%d.%H%M%S", time.localtime())
    docker_run_name = "%s-%s" % (proj,docker_run_time)
    docker_run_arg = "--name %s %s" % (docker_run_name,docker_run_arg)
    docker_run = "docker run  %s %s %s" % (docker_run_arg,docker_run_image,docker_run_cmd)
    os.chdir(CONFIG_BASE_DIR)
    docker_deploy(hosts,proj,tag,docker_run,docker_image_url,wait_times,eureka_url,app_spring_name,exec_mode,log_file)


if __name__ == "__main__":
    main(sys.argv[1:])



