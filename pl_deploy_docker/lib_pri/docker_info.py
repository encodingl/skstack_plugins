#!/usr/bin/env python
#coding=utf-8


import json
import time, pytz, datetime
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.auth.credentials import StsTokenCredential

from google.cloud import artifactregistry_v1
from google.oauth2 import service_account



def get_shanghai_timestamp(timestamp):
        time_zone = pytz.timezone('Asia/Shanghai')
        d = pytz.datetime.datetime.fromtimestamp(timestamp/1000, time_zone)
        timeArray = d.strftime("%Y-%m-%d %H:%M:%S")
        return timeArray


def docker_aliyun_repo_tags(repo_namespace, repo_name, access_key, access_secret, region_id, pagesize):
    credentials = AccessKeyCredential(access_key, access_secret)
    client = AcsClient(region_id=region_id, credential=credentials)

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_method('GET')
    request.set_protocol_type('https') # https | http
    request.set_domain("cr.%s.aliyuncs.com" %(region_id))
    request.set_version('2016-06-07')
    request.add_query_param('Page', "1")
    request.add_query_param('PageSize', pagesize)
    request.add_header('Content-Type', 'application/json')

    request.set_uri_pattern("/repos/%s/%s/tags" %(repo_namespace,repo_name))
    response = client.do_action_with_exception(request)
    response_json=json.loads(str(response, encoding = 'utf-8'))
    res_list=response_json["data"]["tags"]
    list=[]
    list2=[]
    for i in res_list:
        # res_l_i=i["tag"] + " (" + str(i["digest"]) + ", " + str(get_shanghai_timestamp(i["imageUpdate"])) + ", " + str(i["imageId"]) + ", " + str(i["imageSize"]) + ")"
        res_l_i=i["tag"] + " (" + str(i["digest"]) +  ")"
        if i["tag"] == "latest":
            list2.append(res_l_i)
        else:
            list.append(res_l_i)

    list.insert(1,list2[0])
    return list


def docker_gcp_repo_list_tags_page_token(key_json_path,pagetoken,parent):
    credentials = service_account.Credentials.from_service_account_file(key_json_path)
    
    # Create a client
    client = artifactregistry_v1.ArtifactRegistryClient(credentials=credentials)

    # Initialize request argument(s)
    if len(pagetoken) == 0:
        request = artifactregistry_v1.ListTagsRequest(parent=parent)
    else:
        request = artifactregistry_v1.ListTagsRequest(parent=parent, page_token=pagetoken)
    
    # Make the request
    page_result = client.list_tags(request=request)
        
    return page_result.tags, page_result.next_page_token

def docker_gcp_repo_list_tags(key_json_path,gcp_proj,region_id,repo_namespace,repo_name,pagesize):
    parent = "projects/%s/locations/%s/repositories/%s/packages/%s" %(gcp_proj,region_id,repo_namespace,repo_name)
    next_page_token=""
    tags_list=[]
    npt=True
    while npt:
        tags,next_page_token = docker_gcp_repo_list_tags_page_token(key_json_path,next_page_token,parent)
        tags_list.extend(tags)
        if len(next_page_token) != 0:
            npt=True            
        else:
            npt=False
    list_a = []
    list = []
    for i in tags_list[-int(pagesize):]:
        tags_name = str(i.name.split("/")[-1:][0])
        tags_version = str(i.version.split("sha256:")[-1:][0])
        res_l_i = tags_name + " (" + tags_version + ")"      
        if tags_name == "latest":
            list_a.append(res_l_i)
        else:
            list.append(res_l_i)  
    list.reverse()
    list.insert(1, list_a[0])
    return list


def docker_tag_format(tag):
    if tag == "latest":
        return tag
    else:
        tag_f = tag.split(" (")[0]
        return tag_f