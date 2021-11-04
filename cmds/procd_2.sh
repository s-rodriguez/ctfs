#!/bin/bash

# 1) ----------- install procdump
sudo apt-get install procdump -y > /tmp/file.txt

echo "finished 1)" >> /tmp/file.txt

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net

# 2) ----------- test that procdump works

procdump > /tmp/file.txt

echo "finished 2)" >> /tmp/file.txt

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net
