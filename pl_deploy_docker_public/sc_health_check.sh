#!/bin/bash
# this script have been used for  service status check
ServicePort=$1
CheckUrl=$2
MaxCheckTime=$3

#waiting for App startup
sleep 10s
checktimes=$[MaxCheckTime/5]
for(( i=1; i<=$checktimes;i++ ))
    do
        hostname=`hostname`
        status=`curl -sIL -w "%{http_code}\n" -o /dev/null http://$hostname:$ServicePort/$CheckUrl`
        if [ -n "$status" ];then
            if [ $status -eq 200 ];then
                echo successful;
                exit 0;
            fi

        fi
        sleep 5s
    done
echo "failed"
exit 1