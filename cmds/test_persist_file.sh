#!/bin/sh

# install gdb to provide gcore
# sudo is passwordless according to doc
sudo apt-get install gdb > /tmp/file.txt
echo "------------------" >> /tmp/file.txt
gdb -v >> /tmp/file.txt

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net
