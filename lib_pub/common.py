#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import sys



def load_pri_json_conf(CONFIG_BASE_DIR,env,key):
    config_file = env+"_conf.json"
    abs_config_file = os.path.join(CONFIG_BASE_DIR, 'conf', config_file)
    if os.path.exists(abs_config_file):
        with open(abs_config_file, "r") as f:
            d=json.load(f)
            if d.__contains__(key):
                v1 = d[key]
                return v1
            else:
                print(("%s is not exist in %s" % (key,abs_config_file)))
                sys.exit(1)
        
    else:
        print(("%s is not exist" % abs_config_file))
        sys.exit(1)
        
def load_pub_json_conf(env,key):
    CONFIG_PUB_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_file = env+"_conf.json"
    abs_config_file = os.path.join(CONFIG_PUB_DIR, 'conf_pub', config_file)
    if os.path.exists(abs_config_file):
        with open(abs_config_file, "r") as f:
            d=json.load(f)
            if d.__contains__(key):
                v1 = d[key]
                return v1
            else:
                print(("%s is not exist in %s" % (key,abs_config_file)))
                sys.exit(1)
        
    else:
        print(("%s is not exist" % abs_config_file))
        sys.exit(1)
        

def load_pri_json_conf_keys(CONFIG_BASE_DIR,env,keyword):
    config_file = env+"_conf.json"
    abs_config_file = os.path.join(CONFIG_BASE_DIR, 'conf', config_file)
    if os.path.exists(abs_config_file):
        with open(abs_config_file, "r") as f:
            d=json.load(f)
            list_keys = list(d.keys())
            if keyword == "None":   
                return list_keys
            else:
                return [key for key in list_keys if keyword in key]
        
    else:
        print(("%s is not exist" % abs_config_file))
        sys.exit(1)
