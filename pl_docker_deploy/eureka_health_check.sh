#!/bin/bash
# this script have been used for sprintboot service status check
AppInstance=$1
#waiting for App startup
sleep 10s
for(( i=1; i<=24;i++ ))
    do
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
