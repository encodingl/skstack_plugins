#!/bin/bash
# this script have been used for sprintboot service status check
EurekaUrl=$1
AppSpringName=$2
MaxCheckTime=$3
#waiting for App startup
sleep 10s
checktimes=$[MaxCheckTime/5]
for(( i=1; i<=$checktimes;i++ ))
    do
        hostname=`hostname`
        AppInstance=`curl -s $EurekaUrl |grep $hostname:$AppSpringName:|awk -F / '{print $3}'`
        status=`curl -s http://$AppInstance/health/status`
        if [ -n "$status" ];then
            if [ $status -eq 1 ];then
                echo successful;
                exit 0;
            fi

        fi
        sleep 5s
    done
echo "failed"
exit 1
