#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2018年6月12日 @author: skipper
'''
import paramiko

def ssh_cmd_func(host,port,username,password,cmd,rsa_key):
    try:
#         paramiko.util.log_to_file(log)
        #创建ssh客户端
        client = paramiko.SSHClient()
        #第一次ssh远程时会提示输入yes或者no
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        if  password:
            client.connect(host, port, username=username, password=password, timeout=20)
        else:
            key_file = paramiko.RSAKey.from_private_key_file(rsa_key)
            client.connect(host, port, username=username, pkey=key_file, timeout=20)
         
        stdin, stdout,stderr = client.exec_command(cmd,get_pty=True)
        
    
        while 1:
           
            result = stdout.readline()
          
            if len(result) == 0:
                break
            print(result)
     
            
    except Exception as e:
        print(e)
    finally:
        client.close()

if __name__=="__main__":
    host = "172.28.28.127"
    username = "root"
    password = ""
    port = 22
    rsa_key = "/root/.ssh/id_rsa"
    cmd = "ansible gtest -a 'date'"
    cmd2 = "echo 'haha'&&sleep 5s&&echo 'bb'"
    ssh_cmd_func(host,port,username,password,cmd2,rsa_key)
